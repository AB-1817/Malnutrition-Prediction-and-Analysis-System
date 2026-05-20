"""
Groq-powered Chatbot for Food Safety & Malnutrition Prediction System
Integrates with Flask API for predictions and explanations
"""
import json
import re
import logging
from typing import Dict, List, Tuple
from groq import Groq

logger = logging.getLogger(__name__)

class FoodSafetyChatbot:
    def __init__(self, groq_api_key: str, prediction_engine=None):
        """
        Initialize Groq chatbot for Food Safety system

        Args:
            groq_api_key: Your Groq API key
            prediction_engine: PredictionEngine instance for predictions
        """
        self.client = Groq(api_key=groq_api_key)
        self.prediction_engine = prediction_engine
        self.conversation_history = []
        self.model = "llama-3.3-70b-versatile"  # Current Groq model

        self.system_prompt = """You are an expert AI assistant for the Food Safety & Malnutrition Risk Assessment System.

Your capabilities:
1. **Make Predictions**: When users provide health/nutrition metrics, extract numerical values and make risk predictions
2. **Explain Results**: Provide actionable insights about food safety and malnutrition risk factors
3. **Answer Questions**: Provide expert knowledge about:
   - Stunting, wasting, and underweight indicators
   - Malnutrition risk assessment
   - Food safety best practices
   - Nutrition improvement strategies
   - Regional nutrition trends

Required Features for Predictions (0-100 scale):
- stunting: % of children with stunted growth
- wasting: % of children with acute malnutrition
- underweight: % of children below healthy weight
- overweight: % of overweight population
- stunting_avg: average stunting indicator
- wasting_avg: average wasting indicator
- underweight_avg: average underweight indicator
- undernourishment_pct: % of undernourished population

Risk Levels: Critical Risk, High Risk, Moderate Risk, Low Risk, Very Low Risk

When users ask for predictions:
1. Extract all 8 numerical values from their input
2. Return JSON format: {"action": "predict", "features": {...}}
3. Otherwise, respond naturally with expert advice

Be empathetic, informative, and action-oriented in your responses."""

    def extract_prediction_request(self, user_input: str) -> Tuple[bool, Dict]:
        """
        Use Groq to extract prediction features from natural language

        Args:
            user_input: User's natural language input

        Returns:
            Tuple of (has_prediction_request, features_dict)
        """
        extraction_prompt = f"""Analyze this user input and extract prediction features for food safety assessment.

User input: "{user_input}"

If the input contains health/nutrition metrics, extract these 8 values (0-100 scale):
1. stunting - % of children with stunted growth
2. wasting - % of children with acute malnutrition
3. underweight - % of children below healthy weight
4. overweight - % of overweight population
5. stunting_avg - average stunting indicator
6. wasting_avg - average wasting indicator
7. underweight_avg - average underweight indicator
8. undernourishment_pct - % of undernourished population

Respond ONLY in this JSON format:
{{"is_prediction_request": true/false, "features": {{"stunting": value, "wasting": value, ...}}, "country": "name if mentioned"}}

If any value is missing or user asks general questions, set is_prediction_request to false."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            response_text = response.choices[0].message.content.strip()

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if data.get('is_prediction_request'):
                    return True, data.get('features', {})

            return False, {}

        except Exception as e:
            logger.error(f"Feature extraction error: {str(e)}")
            return False, {}

    def format_prediction_response(self, prediction_result: Dict, explanation: Dict, country: str = "") -> str:
        """
        Format prediction results for natural language response

        Args:
            prediction_result: Output from predict_with_confidence
            explanation: Output from get_shap_explanation
            country: Country name if provided

        Returns:
            Formatted natural language response
        """
        risk_level = prediction_result['risk_level']
        confidence = prediction_result['confidence'] * 100

        # Risk level guidance
        risk_guidance = {
            'Critical Risk': 'Immediate intervention required. Urgent policy action needed.',
            'High Risk': 'Significant concern. Priority interventions recommended.',
            'Moderate Risk': 'Notable challenges. Targeted programs advised.',
            'Low Risk': 'Satisfactory status. Continue monitoring.',
            'Very Low Risk': 'Excellent food safety and nutrition status.'
        }

        guidance = risk_guidance.get(risk_level, '')

        # Format top drivers
        top_drivers = explanation.get('top_drivers', [])
        drivers_text = ', '.join([f"{d['feature']} ({d['importance']:.2f})" for d in top_drivers[:3]])

        # Probability distribution
        probs = prediction_result.get('probabilities', {})
        prob_text = ', '.join([f"{k}: {v*100:.1f}%" for k, v in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]])

        response = f"""
**Risk Assessment Result** {'for ' + country if country else ''}

🎯 **Risk Level**: {risk_level}
📊 **Confidence**: {confidence:.1f}%

**Assessment**: {guidance}

**Key Risk Factors** (in order of importance):
{drivers_text}

**Probability Distribution** (top 3):
{prob_text}

**Recommendations**:
- Monitor {drivers_text.split(',')[0].split('(')[0].strip()} closely
- Implement targeted interventions for identified risk factors
- Continue regular monitoring and assessment
"""
        return response

    def chat(self, user_message: str) -> str:
        """
        Main chatbot interface - processes user input and returns response

        Args:
            user_message: User's message

        Returns:
            Chatbot's response
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Check if this is a prediction request
        is_prediction, features = self.extract_prediction_request(user_message)

        prediction_context = ""
        if is_prediction and self.prediction_engine:
            try:
                import numpy as np

                # Extract country name if mentioned
                country_match = re.search(r'(country|for|in)\s+([A-Za-z\s]+?)(?:,|with|has|$)', user_message, re.IGNORECASE)
                country = country_match.group(2).strip() if country_match else ""

                # Validate features
                valid, msg = self.prediction_engine.validate_features(features)
                if not valid:
                    return f"⚠️ Invalid input: {msg}. Please provide values between 0-100 for all metrics."

                # Create feature vector
                feature_vector = np.array([[
                    features.get('stunting', 0),
                    features.get('wasting', 0),
                    features.get('underweight', 0),
                    features.get('overweight', 0),
                    features.get('stunting_avg', 0),
                    features.get('wasting_avg', 0),
                    features.get('underweight_avg', 0),
                    features.get('undernourishment_pct', 0)
                ]])

                # Get prediction
                prediction = self.prediction_engine.predict_with_confidence(feature_vector)

                # Get explanation
                explanation = self.prediction_engine.get_shap_explanation(feature_vector)

                # Format response
                prediction_context = self.format_prediction_response(prediction, explanation, country)

            except Exception as e:
                logger.error(f"Prediction error: {str(e)}")
                return f"❌ Error processing prediction: {str(e)}"

        # Prepare messages for Groq (include system prompt in messages)
        groq_messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        groq_messages.extend(self.conversation_history if self.conversation_history else [
            {
                "role": "user",
                "content": user_message + (f"\n\nPrediction Result: {prediction_context}" if prediction_context else "")
            }
        ])

        try:
            # Get response from Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=groq_messages,
                temperature=0.7,
                max_tokens=1000
            )

            assistant_message = response.choices[0].message.content

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Combine prediction context with Groq response if prediction was made
            if prediction_context:
                return prediction_context + "\n\n**Analysis**:\n" + assistant_message

            return assistant_message

        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return f"❌ Error generating response: {str(e)}"

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
