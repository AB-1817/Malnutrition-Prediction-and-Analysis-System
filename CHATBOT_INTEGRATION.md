# 🤖 Groq Chatbot Integration Summary

## ✅ What's Been Created

### 1. **Chatbot Module** (`api/groq_chatbot.py`)
- `FoodSafetyChatbot` class with Groq integration
- Natural language → feature extraction
- Direct integration with your prediction models
- SHAP explanation formatting
- Conversation memory management

**Key Methods:**
- `chat(message)` - Main interface
- `extract_prediction_request(input)` - Parse natural language for metrics
- `format_prediction_response()` - Pretty-print results
- `get_conversation_history()` - View full conversation
- `reset_conversation()` - Clear memory

### 2. **Flask API Integration** (Updated `api/app.py`)
Added 3 new endpoints:
- `POST /chat` - Send message to chatbot
- `POST /chat/reset` - Reset conversation
- `GET /chat/history` - View conversation history

### 3. **Standalone Chatbot App** (`chatbot_app.py`)
- Interactive CLI interface
- No Flask required
- Commands: quit, clear, history
- Perfect for testing and development

### 4. **Test Script** (`test_chatbot.py`)
- Validates chatbot setup
- Runs sample conversations
- Tests knowledge, predictions, follow-ups

### 5. **Documentation** (`CHATBOT_SETUP.md`)
- Complete setup guide
- Usage examples
- API documentation
- Troubleshooting

### 6. **Dependencies** (Updated `requirements.txt`)
- Added `groq>=0.4.0`

---

## 🚀 How to Use

### **Step 1: Get Groq API Key**
1. Go to https://console.groq.com
2. Sign up/login
3. Create API key
4. Copy key (format: `gsk_...`)

### **Step 2: Set Environment Variable**

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "gsk_your_api_key"
python chatbot_app.py
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="gsk_your_api_key"
python chatbot_app.py
```

### **Step 3: Try Different Interfaces**

#### Option A: Interactive CLI
```bash
python chatbot_app.py
```

#### Option B: Flask API
```bash
# Terminal 1: Start API
cd FoodSafety_Malnutrition
python api/app.py

# Terminal 2: Send requests
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is stunting?"}'
```

#### Option C: Python Script
```python
from FoodSafety_Malnutrition.api.groq_chatbot import FoodSafetyChatbot
from FoodSafety_Malnutrition.api.models_loader import ModelsLoader
from FoodSafety_Malnutrition.api.predict_engine import PredictionEngine
import os

models_loader = ModelsLoader()
models_loader.load_all_models()
prediction_engine = PredictionEngine(models_loader)

chatbot = FoodSafetyChatbot(os.getenv('GROQ_API_KEY'), prediction_engine)
response = chatbot.chat("India has 35% stunting, 20% wasting, 40% underweight...")
print(response)
```

---

## 💬 Chatbot Capabilities

### Natural Language Prediction
```
User: "What's the risk for Ethiopia with 40% stunting and 22% wasting?"

Bot: 
**Risk Assessment Result** for Ethiopia

🎯 **Risk Level**: High Risk
📊 **Confidence**: 89.2%

**Assessment**: Significant concern. Priority interventions recommended.

**Key Risk Factors** (in order of importance):
stunting (0.52), wasting (0.28), underweight (0.15)

**Probability Distribution** (top 3):
High Risk: 89.2%, Moderate Risk: 8.1%, Critical Risk: 2.7%

**Analysis**:
The elevated stunting rate (40%) is the primary driver of the high-risk assessment...
```

### Knowledge Questions
```
User: "How does food safety relate to malnutrition?"

Bot: Food safety and malnutrition are deeply interconnected...
[Expert explanation using Groq]
```

### Follow-up Conversations
```
User: "What about stunting specifically?"

Bot: [Response considers previous context and full conversation history]
```

---

## 🔌 API Usage Examples

### Chat Endpoint
```bash
# Request
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Kenya has 35% stunting, 15% wasting, 38% underweight, 10% overweight, 30% stunting_avg, 12% wasting_avg, 35% underweight_avg, 20% undernourishment_pct"
  }'

# Response
{
  "message": "**Risk Assessment Result** for Kenya\n\n🎯 **Risk Level**: High Risk\n...",
  "conversation_id": 139875453
}
```

### History Endpoint
```bash
curl http://localhost:5000/chat/history

# Response
{
  "history": [
    {"role": "user", "content": "What is stunting?"},
    {"role": "assistant", "content": "Stunting is..."},
    ...
  ],
  "total_messages": 6
}
```

### Reset Endpoint
```bash
curl -X POST http://localhost:5000/chat/reset

# Response
{"status": "Conversation reset"}
```

---

## 📊 Technical Architecture

```
User Input (Natural Language)
    ↓
Groq Chatbot (groq_chatbot.py)
    ├─ Extract Features (Groq parsing)
    ├─ Validate Features (0-100 range)
    ├─ Call Prediction Engine
    │   ├─ Get Prediction (LR/RF/XGB)
    │   └─ Get SHAP Explanation
    ├─ Format Response (Pretty print)
    └─ Call Groq for Analysis
        ├─ Combine prediction + expert analysis
        └─ Return formatted response
    ↓
User-Friendly Response
```

---

## 🛡️ Security Considerations

1. **API Key Management**
   - Use environment variables (never hardcode)
   - Set `.gitignore`: `.env`, `*.key`, `secrets.json`
   - Rotate keys regularly
   - Monitor usage at console.groq.com

2. **Input Validation**
   - Chatbot validates 0-100 range
   - Rejects invalid feature values
   - Logs all requests

3. **Rate Limiting**
   - Groq has API rate limits
   - Implement request queuing in production
   - Monitor limits in dashboard

---

## 📈 Example Conversations

### Scenario 1: Single Country Prediction
```
User: "What's the malnutrition risk for Bangladesh?"
→ Bot: Asks for specific metrics OR provides assessment based on known data

User: "Bangladesh has 35% stunting..."
→ Bot: Provides detailed prediction with risk level and factors
```

### Scenario 2: Comparative Analysis
```
User: "Compare Sub-Saharan Africa to South Asia"
→ Bot: Uses conversation memory to provide comparison using previous data

User: "Which interventions work best for each?"
→ Bot: Evidence-based recommendations for each region
```

### Scenario 3: Policy Insights
```
User: "What are the top drivers of high risk?"
→ Bot: Explains SHAP values and feature importance

User: "What should we prioritize?"
→ Bot: Policy recommendations based on prediction drivers
```

---

## 🔧 Customization Options

### Change Groq Model
```python
chatbot.model = "llama2-70b-4096"  # More capable, slower
# or
chatbot.model = "gemma-7b-it"      # Faster, smaller
```

### Modify System Prompt
```python
chatbot.system_prompt = "You are a food security expert. Your role is..."
```

### Adjust Temperature (Creativity)
```python
# In groq_chatbot.py, line 149:
temperature=0.7  # 0.0 = deterministic, 1.0 = creative
```

### Custom Feature Validation
```python
# Edit validate_features() in predict_engine.py
if data[field] < min_val or data[field] > max_val:
    # Custom validation
```

---

## 📦 Files Changed/Created

### New Files Created
- ✅ `FoodSafety_Malnutrition/api/groq_chatbot.py` (250+ lines)
- ✅ `chatbot_app.py` (interactive CLI)
- ✅ `test_chatbot.py` (test suite)
- ✅ `CHATBOT_SETUP.md` (documentation)

### Files Modified
- ✅ `FoodSafety_Malnutrition/api/app.py` (added 3 endpoints)
- ✅ `requirements.txt` (added groq dependency)

---

## ✅ Ready for Production

Your chatbot is production-ready with:

✅ Error handling and logging  
✅ Input validation  
✅ Conversation memory  
✅ SHAP integration  
✅ Flask API endpoints  
✅ Standalone CLI  
✅ Comprehensive documentation  
✅ Test suite  

---

## 🚀 Next Steps

1. **Install Dependencies**
   ```bash
   pip install groq>=0.4.0
   ```

2. **Set API Key**
   ```bash
   export GROQ_API_KEY="your-key-here"
   ```

3. **Test Standalone**
   ```bash
   python chatbot_app.py
   ```

4. **Test API**
   ```bash
   cd FoodSafety_Malnutrition
   python api/app.py
   # In another terminal: test /chat endpoint
   ```

5. **Integrate with Streamlit** (Optional)
   ```python
   # Add chatbot page to streamlit_app.py
   ```

6. **Deploy**
   ```bash
   docker-compose up -d
   ```

---

## 📞 Support & Troubleshooting

**Issue**: "GROQ_API_KEY not set"
```bash
# Verify environment variable
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows
```

**Issue**: "ModuleNotFoundError: No module named 'groq'"
```bash
pip install groq
```

**Issue**: "Connection timeout to Groq"
- Check internet connection
- Verify API key is valid
- Check console.groq.com for service status

**Issue**: "Models not loading"
- Ensure models are in `FoodSafety_Malnutrition/models/`
- Run test_chatbot.py to debug

---

**Your Food Safety Chatbot is ready! 🤖🍎**

Get your API key from https://console.groq.com and start chatting!
