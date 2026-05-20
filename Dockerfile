# Multi-stage Dockerfile for Food Safety API & Streamlit Dashboard

# ==================== STAGE 1: BASE IMAGE ====================
FROM python:3.12-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ==================== EXPOSE PORTS ====================
EXPOSE 5000 8501

# ==================== HEALTHCHECK ====================
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# ==================== START SERVICES ====================
CMD ["sh", "-c", "python FoodSafety_Malnutrition/api/app.py & streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
