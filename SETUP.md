# 🚀 Setup Guide

This guide will help you set up the Malnutrition Prediction and Analysis System on your local machine.

## 📋 Prerequisites

### Required Software
- **Python 3.9 or higher** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (comes with Python)

### Optional Software
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/)) - For containerized deployment
- **Jupyter Notebook** - For running notebooks interactively
- **VS Code** or **PyCharm** - Recommended IDEs

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

---

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git
cd Malnutrition-Prediction-and-Analysis-System
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt
```

**Note**: Installation may take 5-10 minutes depending on your internet speed.

### Step 4: Verify Installation

```bash
python -c "import tensorflow; import sklearn; import streamlit; print('All packages installed successfully!')"
```

---

## 📊 Data Setup

### Option 1: Use Sample Data (Quick Start)

The repository includes sample processed data in `FoodSafety_Malnutrition/data/processed/`.

### Option 2: Generate Data from Notebooks

Run the data collection notebook:
```bash
jupyter notebook FoodSafety_Malnutrition/notebooks/01_Data_Collection_Merging.ipynb
```

### Option 3: Download Full Dataset

Due to GitHub file size limits, large datasets are hosted externally:

1. Download from [Google Drive Link] (to be added)
2. Extract to `FoodSafety_Malnutrition/data/`

---

## 🤖 Model Setup

### Option 1: Use Pre-trained Models

Pre-trained models are included in `FoodSafety_Malnutrition/models/`.

### Option 2: Train Models from Scratch

Run notebooks 2-13 in sequence:
```bash
jupyter notebook FoodSafety_Malnutrition/notebooks/
```

**Training Time Estimates:**
- Notebooks 1-6: ~2-3 hours
- Notebooks 7-10: ~1-2 hours
- Notebooks 11-13: ~3-4 hours (requires GPU for faster training)

---

## 🌐 Running the Application

### Option 1: Streamlit Dashboard (Recommended)

```bash
streamlit run streamlit_app.py
```

Open browser to: **http://localhost:8501**

### Option 2: Flask API

```bash
python FoodSafety_Malnutrition/api/app.py
```

API available at: **http://localhost:5000**

Test the API:
```bash
curl http://localhost:5000/health
```

### Option 3: Both Services

**Terminal 1 (API):**
```bash
python FoodSafety_Malnutrition/api/app.py
```

**Terminal 2 (Dashboard):**
```bash
streamlit run streamlit_app.py
```

---

## 🐳 Docker Setup (Advanced)

### Prerequisites
- Docker Desktop installed and running

### Build and Run

```bash
# Build containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- Dashboard: http://localhost:8501
- API: http://localhost:5000
- PostgreSQL: localhost:5432

---

## 🤖 Chatbot Setup (Optional)

The AI chatbot requires a Groq API key.

### Step 1: Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key

### Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Windows:**
```bash
echo GROQ_API_KEY=your_key_here > .env
```

**macOS/Linux:**
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

### Step 3: Test Chatbot

```bash
python test_chatbot.py
```

---

## 🧪 Testing the Installation

### Test 1: Import Check
```bash
python -c "from FoodSafety_Malnutrition.api.models_loader import ModelsLoader; print('Models loader OK')"
```

### Test 2: API Health Check
```bash
# Start API first
python FoodSafety_Malnutrition/api/app.py

# In another terminal
curl http://localhost:5000/health
```

### Test 3: Dashboard Launch
```bash
streamlit run streamlit_app.py
```

### Test 4: Run Unit Tests
```bash
pytest tests/ -v
```

---

## 🔧 Troubleshooting

### Issue: TensorFlow Installation Fails

**Solution:**
```bash
# For Windows
pip install tensorflow-cpu

# For macOS (M1/M2)
pip install tensorflow-macos tensorflow-metal
```

### Issue: Port Already in Use

**Solution:**
```bash
# Change Streamlit port
streamlit run streamlit_app.py --server.port=8502

# Change Flask port
# Edit app.py: app.run(port=5001)
```

### Issue: Module Not Found

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: CUDA/GPU Not Detected

**Solution:**
```bash
# Install CUDA-enabled TensorFlow
pip install tensorflow-gpu

# Verify GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Issue: Jupyter Kernel Not Found

**Solution:**
```bash
# Install ipykernel
pip install ipykernel

# Add virtual environment to Jupyter
python -m ipykernel install --user --name=.venv
```

---

## 📚 Next Steps

After successful setup:

1. **Explore the Dashboard**: Navigate through all 8 pages
2. **Run Notebooks**: Execute notebooks 1-13 to understand the pipeline
3. **Test API**: Try prediction endpoints with sample data
4. **Read Documentation**: Check IMPLEMENTATION_SUMMARY.md for details
5. **Customize**: Modify models, add features, or integrate new data

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Documentation**: Review README.md and other docs
2. **Search Issues**: Look for similar problems on GitHub
3. **Create Issue**: Open a new issue with details
4. **Contact Team**: Email akashbhuyan1817@gmail.com

---

## 🎓 Learning Resources

- **Streamlit**: https://docs.streamlit.io/
- **Flask**: https://flask.palletsprojects.com/
- **TensorFlow**: https://www.tensorflow.org/tutorials
- **scikit-learn**: https://scikit-learn.org/stable/tutorial/
- **Docker**: https://docs.docker.com/get-started/

---

**Setup complete! You're ready to predict malnutrition risks! 🌍**
