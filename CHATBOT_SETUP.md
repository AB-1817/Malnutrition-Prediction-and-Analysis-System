# 🤖 Groq-Powered Chatbot for Food Safety & Malnutrition System

This chatbot integrates **Groq's fast LLM API** with your Food Safety & Malnutrition Risk Assessment System to provide:

✅ **Natural Language Predictions** - Ask about risk in plain English  
✅ **Intelligent Explanations** - Understand which factors drive predictions  
✅ **Domain Expertise** - Get advice on nutrition, food safety, and policy  
✅ **Conversation Memory** - Context-aware multi-turn conversations  

---

## 🚀 Quick Start

### 1. Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up/login with your account
3. Create an API key in the "API Keys" section
4. Copy your key (starts with `gsk_`)

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "gsk_your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_your_api_key_here
```

**Linux/Mac (Bash):**
```bash
export GROQ_API_KEY="gsk_your_api_key_here"
```

### 3. Install Dependencies

```bash
pip install groq>=0.4.0
# Or install all requirements
pip install -r requirements.txt
```

---

## 📱 Usage Options

### Option 1: Standalone Chatbot (Interactive CLI)

```bash
python chatbot_app.py
```

**Example conversation:**
```
You: What's the food safety risk for a country with 35% stunting and 20% wasting?

Bot: **Risk Assessment Result**

🎯 **Risk Level**: High Risk
📊 **Confidence**: 87.3%

**Assessment**: Significant concern. Priority interventions recommended.

**Key Risk Factors** (in order of importance):
stunting (0.45), underweight (0.32), wasting (0.21)

**Probability Distribution** (top 3):
High Risk: 87.3%, Moderate Risk: 9.2%, Critical Risk: 3.5%

**Analysis**:
The elevated stunting rate is the primary driver of the high-risk assessment...
```

### Option 2: Flask API Endpoint

**Start your Flask API:**
```bash
cd FoodSafety_Malnutrition
python api/app.py
```

**Send a chat request:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the risk for India with 35% stunting, 20% wasting?"}'
```

**Response:**
```json
{
  "message": "**Risk Assessment Result** for India\n\n🎯 **Risk Level**: High Risk\n...",
  "conversation_id": 12345
}
```

### Option 3: Python Integration

```python
from FoodSafety_Malnutrition.api.groq_chatbot import FoodSafetyChatbot
from FoodSafety_Malnutrition.api.models_loader import ModelsLoader
from FoodSafety_Malnutrition.api.predict_engine import PredictionEngine
import os

# Initialize
models_loader = ModelsLoader()
models_loader.load_all_models()
prediction_engine = PredictionEngine(models_loader)

chatbot = FoodSafetyChatbot(
    groq_api_key=os.getenv('GROQ_API_KEY'),
    prediction_engine=prediction_engine
)

# Chat
response = chatbot.chat("What's the malnutrition risk for Bangladesh?")
print(response)
```

---

## 📊 Chatbot Capabilities

### 1. **Risk Predictions**
Ask about food safety/nutrition metrics and get instant predictions:
- "What is the stunting risk in Sub-Saharan Africa?"
- "Predict risk for a country with 40% underweight"
- "Nigeria: 35% stunting, 18% wasting, 38% underweight, 12% overweight, 30% stunting_avg, 15% wasting_avg, 35% underweight_avg, 25% undernourishment_pct"

### 2. **Explain Predictions**
Understand which factors matter most:
- "Why is this region at high risk?"
- "Which metrics are most important for this prediction?"
- "What are the top drivers of malnutrition risk?"

### 3. **Domain Expertise**
Get answers on nutrition and food safety:
- "What is stunting and why does it matter?"
- "How does malnutrition affect economic development?"
- "What are evidence-based interventions for child nutrition?"
- "How does food safety relate to malnutrition?"

### 4. **Conversation Memory**
Multi-turn conversations with context:
```
You: Tell me about malnutrition in Africa
Bot: [Explanation of African nutrition challenges]

You: What about South Asia?
Bot: [Response considering previous context]

You: How do they compare?
Bot: [Comparative analysis using conversation history]
```

---

## 🔌 API Endpoints

### POST `/chat` - Send Message
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Your question or prediction request"}'
```

**Response:**
```json
{
  "message": "Response text with predictions/explanations",
  "conversation_id": 123456789
}
```

### POST `/chat/reset` - Clear History
```bash
curl -X POST http://localhost:5000/chat/reset
```

### GET `/chat/history` - View Conversation
```bash
curl http://localhost:5000/chat/history
```

**Response:**
```json
{
  "history": [
    {"role": "user", "content": "Your message"},
    {"role": "assistant", "content": "Bot response"}
  ],
  "total_messages": 2
}
```

---

## 🎯 Example Prompts

### Prediction Requests
1. **Single Country**: "What's the risk for Kenya with 35% stunting and 18% wasting?"
2. **Specific Metrics**: "Stunting: 40%, Wasting: 25%, Underweight: 45%, Overweight: 10%, stunting_avg: 35%, wasting_avg: 20%, underweight_avg: 40%, undernourishment_pct: 30%"
3. **Regional Query**: "East Africa has 32% stunting, 15% wasting, 38% underweight, 8% overweight, 28% stunting_avg, 12% wasting_avg, 35% underweight_avg, 22% undernourishment_pct - what's the risk?"

### General Questions
1. **What causes stunting?** - Learn about growth stunting causes
2. **How does malnutrition affect development?** - Policy-relevant insights
3. **What interventions work?** - Evidence-based recommendations
4. **Compare two regions** - Using conversation memory

---

## 🛠️ Configuration

### Model Selection
The chatbot uses Groq's **Mixtral-8x7b** model for:
- ✅ Fast responses (< 2 seconds)
- ✅ Good quality reasoning
- ✅ Cost-effective
- ✅ 32K token context window

### Customization

**Change the Groq model:**
```python
chatbot.model = "llama2-70b-4096"  # Slower but more capable
# or
chatbot.model = "gemma-7b-it"      # Faster, smaller
```

**Modify system prompt:**
```python
chatbot.system_prompt = "Your custom instructions here..."
```

**Adjust feature extraction:**
Edit the `extract_prediction_request()` method in `groq_chatbot.py`

---

## 🔒 Security & Best Practices

1. **Protect Your API Key**
   - Never commit `.env` files to git
   - Use environment variables in production
   - Rotate keys regularly

2. **Rate Limiting**
   - Groq has rate limits (depends on plan)
   - Implement request queuing for production
   - Monitor usage in console.groq.com

3. **Input Validation**
   - Chatbot validates feature ranges (0-100)
   - Rejects invalid inputs gracefully
   - Logs errors for monitoring

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Response Time | 1-3 seconds |
| Model | Mixtral-8x7b |
| Prediction Processing | < 100ms |
| Groq API Latency | 1-2 seconds |
| Total E2E Latency | 1-3 seconds |

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not set"
```bash
# Check if env var is set
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows
```

### "Chatbot not initialized"
Ensure GROQ_API_KEY is set BEFORE starting Flask:
```bash
export GROQ_API_KEY="gsk_..." && python api/app.py
```

### "Import error: groq"
```bash
pip install groq
```

### Slow responses
- Check internet connection
- Verify API key is valid
- Monitor Groq dashboard for errors

---

## 📚 Integration with Your System

The chatbot integrates seamlessly with:

✅ **Your ML Models** - Uses trained LR/RF/XGB for predictions  
✅ **SHAP Explanations** - Provides feature importance breakdown  
✅ **Feature Validation** - Ensures proper input ranges  
✅ **Prediction Engine** - Direct access to all models  
✅ **Flask API** - Works as new endpoint  

---

## 🚀 Next Steps

1. **Add to Streamlit Dashboard** - Create new chatbot page
2. **Setup Docker** - Include groq in Docker image
3. **Add Logging** - Track predictions and interactions
4. **Setup Monitoring** - Alert on API failures
5. **A/B Testing** - Compare Groq vs other LLMs

---

## 📞 Support

- **Groq Issues**: [console.groq.com/docs](https://console.groq.com/docs)
- **API Key Problems**: Check console.groq.com/keys
- **Chatbot Code**: See `FoodSafety_Malnutrition/api/groq_chatbot.py`

---

**Happy chatting! 🤖🍎**
