"""
Flask REST API for Food Safety & Malnutrition Prediction System
Endpoints: /predict, /explain, /batch_predict, /health, /chat
"""
import os
import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from models_loader import ModelsLoader
from predict_engine import PredictionEngine
from groq_chatbot import FoodSafetyChatbot
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize models on startup
models_loader = ModelsLoader()
models_loader.load_all_models()
prediction_engine = PredictionEngine(models_loader)

# Initialize Groq chatbot
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key:
    chatbot = FoodSafetyChatbot(groq_api_key, prediction_engine)
    logger.info("Groq chatbot initialized successfully")
else:
    chatbot = None
    logger.warning("GROQ_API_KEY not set. Chatbot will be unavailable.")

# ==================== HEALTH CHECK ====================
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'models_loaded': models_loader.get_status()
    }), 200

# ==================== SINGLE PREDICTION ====================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Single country prediction endpoint
    Input: JSON with country data
    Output: Risk level, confidence, explanation
    """
    try:
        data = request.get_json()

        # Validate input
        required_fields = ['stunting', 'wasting', 'underweight', 'overweight',
                          'stunting_avg', 'wasting_avg', 'underweight_avg', 'undernourishment_pct']

        if not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Missing required fields. Need: {required_fields}'
            }), 400

        # Create feature vector
        features = np.array([[
            data['stunting'], data['wasting'], data['underweight'], data['overweight'],
            data['stunting_avg'], data['wasting_avg'], data['underweight_avg'],
            data['undernourishment_pct']
        ]])

        # Get prediction
        result = prediction_engine.predict_with_confidence(features)

        return jsonify({
            'risk_level': result['risk_level'],
            'confidence': float(result['confidence']),
            'probability_distribution': {k: float(v) for k, v in result['probabilities'].items()},
            'timestamp': result['timestamp']
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== BATCH PREDICTION ====================
@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Batch predictions for multiple countries
    Input: JSON array of country data
    Output: Array of predictions
    """
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({'error': 'Expected JSON array'}), 400

        predictions = []
        for item in data:
            result =prediction_engine.predict_with_confidence(np.array([
                [item['stunting'], item['wasting'], item['underweight'], item['overweight'],
                 item['stunting_avg'], item['wasting_avg'], item['underweight_avg'],
                 item['undernourishment_pct']]
            ]))
            predictions.append({
                'country': item.get('country', 'Unknown'),
                'risk_level': result['risk_level'],
                'confidence': float(result['confidence'])
            })

        return jsonify({
            'predictions': predictions,
            'total': len(predictions)
        }), 200

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== EXPLAINABILITY ====================
@app.route('/explain', methods=['POST'])
def explain():
    """
    SHAP-based explanation for a prediction
    Shows which features contribute most to the risk level
    """
    try:
        data = request.get_json()

        features = np.array([[
            data['stunting'], data['wasting'], data['underweight'], data['overweight'],
            data['stunting_avg'], data['wasting_avg'], data['underweight_avg'],
            data['undernourishment_pct']
        ]])

        # Get SHAP explanation
        explanation = prediction_engine.get_shap_explanation(features)

        return jsonify({
            'prediction': explanation['prediction'],
            'feature_importance': explanation['feature_importance'],
            'top_drivers': explanation['top_drivers']
        }), 200

    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== MODEL STATUS ====================
@app.route('/status', methods=['GET'])
def status():
    """Get system status and model info"""
    return jsonify({
        'system_status': 'operational',
        'models_loaded': models_loader.get_status(),
        'api_version': '1.0.0'
    }), 200

# ==================== GROQ CHATBOT ====================
@app.route('/chat', methods=['POST'])
def chat():
    """
    Groq-powered chatbot endpoint
    Accepts natural language queries about food safety/nutrition
    Can make predictions if metrics are provided
    """
    if not chatbot:
        return jsonify({'error': 'Chatbot not initialized. Set GROQ_API_KEY environment variable.'}), 503

    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Get chatbot response
        response = chatbot.chat(user_message)

        return jsonify({
            'message': response,
            'conversation_id': id(chatbot.conversation_history)
        }), 200

    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat/reset', methods=['POST'])
def reset_chat():
    """Reset chatbot conversation history"""
    if not chatbot:
        return jsonify({'error': 'Chatbot not initialized'}), 503

    try:
        chatbot.reset_conversation()
        return jsonify({'status': 'Conversation reset'}), 200
    except Exception as e:
        logger.error(f"Reset error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get chatbot conversation history"""
    if not chatbot:
        return jsonify({'error': 'Chatbot not initialized'}), 503

    try:
        history = chatbot.get_conversation_history()
        return jsonify({
            'history': history,
            'total_messages': len(history)
        }), 200
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

# ==================== STARTUP ====================
if __name__ == '__main__':
    logger.info("Starting Food Safety API...")
    logger.info(f"Models status: {models_loader.get_status()}")
    app.run(host='0.0.0.0', port=5000, debug=False)
