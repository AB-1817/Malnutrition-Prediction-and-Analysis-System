# 🌍 Malnutrition Prediction and Analysis System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16%2B-orange.svg)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready AI/ML system for predicting and analyzing global malnutrition risks across 150+ countries. This comprehensive platform combines classical machine learning, deep learning, explainable AI, and geospatial analysis to provide actionable insights for policymakers, researchers, and NGOs working on food security.

## 🎯 Project Overview

This system predicts malnutrition risk levels (**Critical**, **Severe**, **High**, **Moderate**, **Low**) based on key nutrition indicators:
- Stunting rates (%)
- Wasting rates (%)
- Underweight prevalence (%)
- Overweight prevalence (%)
- Undernourishment percentage (%)

**Key Achievements:**
- ✅ **97.88% accuracy** with calibrated Logistic Regression
- ✅ **15+ trained models** (Classical ML + Deep Learning)
- ✅ **944+ country-year observations** across 150+ countries
- ✅ **164K+ India district records** for granular analysis
- ✅ **Production-ready REST API** with Docker support
- ✅ **Interactive dashboard** with real-time predictions
- ✅ **Explainable AI** using SHAP and LIME

---

## ✨ Key Features

### 🤖 Machine Learning Models

| Model | Accuracy | Type | Use Case |
|-------|----------|------|----------|
| Logistic Regression (Calibrated) | 97.88% | Classification | Primary risk predictor |
| Random Forest (Tuned) | 92.1% | Classification | Ensemble member |
| XGBoost (Tuned) | 92.8% | Classification | Gradient boosting |
| ANN | 92.06% | Deep Learning | Tabular classification |
| BiLSTM | 93.3% | Time-Series | Forecasting trends |
| RCNN | 92.75% | Text Classification | Report analysis |
| CNN (ResNet50) | 90%+ | Image Classification | Crop disease detection |

### 📊 Advanced Capabilities
- **Uncertainty Quantification**: Calibrated probabilities with 95% confidence intervals
- **Explainable AI**: SHAP and LIME for feature importance analysis
- **Ensemble Methods**: Voting and stacking classifiers
- **Transfer Learning**: ResNet50, EfficientNetB0 for image analysis
- **Attention Mechanisms**: Multi-head attention in BiLSTM
- **Generative AI**: CTGAN for synthetic data generation
- **Drift Detection**: Automated monitoring and retraining

### 🌐 Production Deployment
- **REST API**: Flask-based with 8 endpoints
- **Interactive Dashboard**: Streamlit with 8 pages
- **AI Chatbot**: Groq-powered conversational interface
- **Docker Support**: Multi-container orchestration
- **Monitoring**: Real-time drift detection and alerts
- **Geospatial Maps**: Interactive world choropleth and heatmaps

---

## 🏗️ Project Structure

```
FoodSafety_Malnutrition/
├── FoodSafety_Malnutrition/
│   ├── api/                          # Flask REST API
│   │   ├── app.py                    # Main API application
│   │   ├── models_loader.py          # Model management
│   │   ├── predict_engine.py         # Prediction logic
│   │   └── groq_chatbot.py           # AI chatbot
│   ├── data/
│   │   ├── processed/                # Cleaned datasets
│   │   ├── tabular/                  # Raw tabular data
│   │   ├── images/                   # Crop disease images
│   │   └── text/                     # Text reports
│   ├── models/                       # Trained model artifacts (15+ models)
│   │   ├── logistic_regression_calibrated.pkl
│   │   ├── random_forest_tuned.pkl
│   │   ├── xgboost_tuned.pkl
│   │   ├── ann_model.h5
│   │   ├── bilstm_attention.h5
│   │   ├── cnn_resnet50_transfer.h5
│   │   └── ...
│   ├── notebooks/                    # 13 Jupyter notebooks
│   │   ├── 01_Data_Collection_Merging.ipynb
│   │   ├── 02_Clustering_Classification.ipynb
│   │   ├── 03_ANN_BiLSTM_RCNN.ipynb
│   │   ├── 04_Explainable_Agentic_AI.ipynb
│   │   ├── 05_Generative_AI.ipynb
│   │   ├── 06_CNN_CropDisease.ipynb
│   │   ├── 07_Cross_Validation_Ensembles.ipynb
│   │   ├── 08_Geospatial_Visualization.ipynb
│   │   ├── 09_Hyperparameter_Optimization.ipynb
│   │   ├── 10_Uncertainty_Quantification.ipynb
│   │   ├── 11_Transfer_Learning_CNN.ipynb
│   │   ├── 12_Attention_BiLSTM.ipynb
│   │   └── 13_Advanced_CNN.ipynb
│   └── outputs/
│       ├── plots/                    # Visualizations (28+ plots)
│       ├── heatmaps/                 # Geospatial heatmaps
│       └── reports/                  # Generated reports
├── monitoring/                       # Model monitoring
│   ├── monitor.py                    # Drift detection
│   └── retraining_trigger.py         # Auto-retraining
├── streamlit_app.py                  # Interactive dashboard
├── docker-compose.yml                # Multi-service deployment
├── Dockerfile                        # Container configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager
- (Optional) Docker and Docker Compose

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git
cd Malnutrition-Prediction-and-Analysis-System
```

2. **Create virtual environment**
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (Optional for chatbot)
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### Running the Application

#### Option 1: Streamlit Dashboard (Recommended for Quick Start)
```bash
streamlit run streamlit_app.py
```
Access at: **http://localhost:8501**

#### Option 2: Flask REST API
```bash
python FoodSafety_Malnutrition/api/app.py
```
API available at: **http://localhost:5000**

#### Option 3: Docker Deployment (Production)
```bash
docker-compose up -d
```
Services:
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:5000
- **PostgreSQL**: localhost:5432

---

## 📡 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/predict` | POST | Single country risk prediction |
| `/batch_predict` | POST | Batch predictions |
| `/explain` | POST | SHAP-based explanation |
| `/status` | GET | Model status |
| `/chat` | POST | AI chatbot conversation |
| `/chat/reset` | POST | Reset chat history |
| `/chat/history` | GET | Get conversation history |

### Example: Single Prediction

**Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "stunting": 35.2,
    "wasting": 18.5,
    "underweight": 28.3,
    "overweight": 5.1,
    "stunting_avg": 32.8,
    "wasting_avg": 16.2,
    "underweight_avg": 25.7,
    "undernourishment_pct": 22.4
  }'
```

**Response:**
```json
{
  "risk_level": "High Risk",
  "confidence": 0.9234,
  "probability_distribution": {
    "Critical Risk": 0.15,
    "Severe Risk": 0.22,
    "High Risk": 0.92,
    "Moderate Risk": 0.08,
    "Low Risk": 0.03
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Example: SHAP Explanation

**Request:**
```python
import requests

data = {
    "stunting": 35.2,
    "wasting": 18.5,
    "underweight": 28.3,
    "overweight": 5.1,
    "stunting_avg": 32.8,
    "wasting_avg": 16.2,
    "underweight_avg": 25.7,
    "undernourishment_pct": 22.4
}

response = requests.post("http://localhost:5000/explain", json=data)
print(response.json())
```

**Response:**
```json
{
  "prediction": "High Risk",
  "feature_importance": {
    "underweight": 1.26,
    "overweight": 1.15,
    "undernourishment_pct": 1.07,
    "stunting": 0.98,
    "wasting": 0.88
  },
  "top_drivers": [
    "Underweight (28.3%) - Primary risk driver",
    "Undernourishment (22.4%) - Secondary factor",
    "Wasting (18.5%) - Contributing factor"
  ]
}
```

---

## Dashboard Features

The Streamlit dashboard includes 8 interactive pages:

1. **📊 Dashboard** - Global risk overview with key metrics
2. **🔮 Predictions** - Interactive risk prediction with sliders
3. **📍 Geospatial** - World maps and country-level analysis
4. **📈 Analytics** - Trends, regional comparisons, correlations
5. **💡 Explainability** - SHAP feature importance visualizations
6. **💬 Chatbot** - AI-powered conversational interface
7. **📚 Notebook Outputs** - Gallery of all generated artifacts
8. **⚙️ System Status** - Model performance and health checks

### Dashboard Screenshots

**Global Risk Map:**
- Interactive choropleth showing risk levels by country
- Color-coded severity (green → red)
- Hover tooltips with detailed indicators

**Prediction Workbench:**
- Adjustable sliders for all 8 input features
- Real-time probability distribution
- Confidence scores and risk classification

**Geospatial Analysis:**
- World risk maps
- India district heatmaps
- Regional breakdown charts

---

## 🔬 Notebooks Overview

### Phase 1: Data & Baseline Models (Notebooks 1-3)
- **01**: Data collection, merging, and preprocessing
- **02**: Clustering (K-Means, Hierarchical, DBSCAN) and classification
- **03**: Deep learning models (ANN, BiLSTM, RCNN)

### Phase 2: Advanced Techniques (Notebooks 4-6)
- **04**: Explainable AI with SHAP and agentic report generation
- **05**: Generative AI with CTGAN for synthetic data
- **06**: CNN for crop disease image classification

### Phase 3: Robustness & Optimization (Notebooks 7-10)
- **07**: Cross-validation and ensemble methods
- **08**: Geospatial visualization and interactive maps
- **09**: Hyperparameter optimization (GridSearch, RandomSearch)
- **10**: Uncertainty quantification and calibration

### Phase 4: Advanced Deep Learning (Notebooks 11-13)
- **11**: Transfer learning with ResNet50
- **12**: Attention mechanisms in BiLSTM
- **13**: Advanced CNN architecture comparison

---

## 🛠️ Technologies Used

### Machine Learning & AI
- **scikit-learn** - Classical ML algorithms
- **XGBoost** - Gradient boosting
- **TensorFlow/Keras** - Deep learning models
- **SHAP** - Model explainability
- **LIME** - Local interpretability
- **CTGAN** - Synthetic data generation

### Data Processing & Visualization
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **Matplotlib/Seaborn** - Static plots
- **GeoPandas** - Geospatial analysis
- **Folium** - Interactive maps

### Web & API
- **Flask** - REST API framework
- **Flask-CORS** - Cross-origin support
- **Streamlit** - Interactive dashboard
- **Groq API** - Conversational AI

### Deployment & DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Database for logging
- **Gunicorn/Waitress** - Production servers

---

## 📈 Model Performance Summary

### Classification Models
| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | 97.88% | 0.98 | 0.98 | 0.98 |
| Random Forest | 92.1% | 0.92 | 0.91 | 0.91 |
| XGBoost | 92.8% | 0.93 | 0.92 | 0.92 |
| ANN | 92.06% | 0.92 | 0.91 | 0.91 |

### Deep Learning Models
| Model | Metric | Performance |
|-------|--------|-------------|
| BiLSTM | MAE | 3.10 |
| BiLSTM + Attention | MAE | 2.95 |
| RCNN | Accuracy | 92.75% |
| CNN (Standard) | Accuracy | 83.27% |
| CNN (ResNet50) | Accuracy | 90%+ |

### Key Insights
- **Top Risk Drivers**: Underweight (1.26), Overweight (1.15), Undernourishment (1.07)
- **Critical Risk Regions**: Sub-Saharan Africa, South Asia
- **Temporal Trends**: Stunting declining, wasting persistent
- **Model Confidence**: 95%+ for high-risk predictions

---

## 🎯 Use Cases

### 1. Policy Makers
- Identify critical risk countries for targeted interventions
- Track progress on SDG 2 (Zero Hunger)
- Allocate resources based on risk severity

### 2. Researchers
- Analyze malnutrition trends over time
- Study causal factors and correlations
- Generate hypotheses for further investigation

### 3. NGOs & International Organizations
- Prioritize regions for humanitarian aid
- Monitor program effectiveness
- Generate donor reports with evidence

### 4. Government Agencies
- National food security monitoring
- Early warning system for crises
- Policy impact assessment

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Groq API for chatbot (optional)
GROQ_API_KEY=your_groq_api_key_here

# Model paths (optional, defaults provided)
MODELS_PATH=FoodSafety_Malnutrition/models
DATA_PATH=FoodSafety_Malnutrition/data

# API configuration
FLASK_ENV=production
FLASK_PORT=5000

# Database (for Docker deployment)
POSTGRES_USER=foodsafety
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=predictions_db
```

### Docker Configuration

The `docker-compose.yml` includes three services:
1. **API** - Flask REST API (port 5000)
2. **Dashboard** - Streamlit app (port 8501)
3. **PostgreSQL** - Database (port 5432)

To customize, edit `docker-compose.yml` and rebuild:
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📚 Documentation

- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete project overview and achievements
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[CHATBOT_SETUP.md](CHATBOT_SETUP.md)** - AI chatbot configuration guide
- **[NOTEBOOKS_1_TO_6_EXPLANATION.md](NOTEBOOKS_1_TO_6_EXPLANATION.md)** - Detailed notebook walkthrough
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference

---

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Test prediction
python test_chatbot.py
```

### Validate Models
```bash
# Run notebook validation
jupyter nbconvert --execute FoodSafety_Malnutrition/notebooks/02_Clustering_Classification.ipynb
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Add unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Data Sources
- **WHO** - World Health Organization nutrition data
- **UNICEF** - Child malnutrition statistics
- **FAO** - Food and Agriculture Organization datasets
- **World Bank** - Global development indicators

### Pre-trained Models
- **ImageNet** - Transfer learning base
- **ResNet50** - Image classification architecture
- **EfficientNet** - Optimized CNN architecture

### Technologies
- **Groq** - Fast AI inference API
- **Streamlit** - Interactive dashboard framework
- **TensorFlow** - Deep learning framework
- **scikit-learn** - Machine learning library

---

## 📧 Contact & Support

For questions, issues, or collaboration opportunities:

- **GitHub Issues**: [Report a bug or request a feature](https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System/issues)
- **Email**: akashbhuyan1817@gmail.com
- **Documentation**: See the `docs/` folder for detailed guides

---

## Project Statistics

- **Lines of Code**: 3,000+
- **Notebooks**: 13
- **Models Trained**: 15+
- **API Endpoints**: 8
- **Dashboard Pages**: 8
- **Visualizations**: 28+
- **Countries Covered**: 150+
- **Data Records**: 165K+

---

## Future Enhancements

- [ ] Real-time data integration with WHO/UNICEF APIs
- [ ] Mobile app for field workers
- [ ] Multi-language support (Spanish, French, Hindi)
- [ ] Advanced time-series forecasting with Prophet
- [ ] Kubernetes deployment for scalability
- [ ] GraphQL API for flexible queries
- [ ] Automated report generation in PDF format
- [ ] Integration with GIS platforms (ArcGIS, QGIS)

---

## Team Members

This project was developed by:

- **Akash Bhuyan** - Project Lead & ML Engineer
- **Rushikesh Kedar** - Data Scientist & API Developer
- **Sujal Khandelwal** - Research & Documentation Lead
- **Namrata Ingole** - Frontend & Visualization Engineer
- **Rutuja Shelke** - Deep Learning Specialist
