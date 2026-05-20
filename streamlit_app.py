"""
Streamlit Interactive Dashboard for Food Safety & Malnutrition Prediction
Run with: streamlit run streamlit_app.py
"""
import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import requests
from PIL import Image
import pickle
import warnings
warnings.filterwarnings('ignore')

# Add API to path for chatbot import
sys.path.insert(0, str(Path(__file__).resolve().parent / "FoodSafety_Malnutrition" / "api"))

# ==================== PATHS ====================
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODELS_DIR = PROJECT_ROOT / "FoodSafety_Malnutrition" / "models"
DEFAULT_DATA_DIR = PROJECT_ROOT / "FoodSafety_Malnutrition" / "data"
MODELS_DIR = Path(os.environ.get("MODELS_PATH", DEFAULT_MODELS_DIR))
DATA_DIR = Path(os.environ.get("DATA_PATH", DEFAULT_DATA_DIR))
OUTPUTS_DIR = PROJECT_ROOT / "FoodSafety_Malnutrition" / "outputs"
PLOTS_DIR = OUTPUTS_DIR / "plots"
REPORTS_DIR = OUTPUTS_DIR / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "FoodSafety_Malnutrition" / "notebooks"

RISK_COLOR_MAP = {
    'Low Risk': '#2ecc71',
    'Moderate Risk': '#f39c12',
    'High Risk': '#e74c3c',
    'Severe Risk': '#c0392b',
    'Critical Risk': '#8b0000'
}

NOTEBOOK_OUTPUTS = [
    {
        "title": "01 - Data Collection & Merging",
        "notebook": "01_Data_Collection_Merging.ipynb",
        "summary": "Creates the cleaned global country dataset and India district dataset used by the rest of the project.",
        "artifacts": [
            "FoodSafety_Malnutrition/data/processed/main_merged.csv",
            "FoodSafety_Malnutrition/data/processed/india_district.csv",
            "FoodSafety_Malnutrition/outputs/plots/distributions.png",
            "FoodSafety_Malnutrition/outputs/plots/correlation_heatmap.png",
        ],
    },
    {
        "title": "02 - Clustering & Classification",
        "notebook": "02_Clustering_Classification.ipynb",
        "summary": "Builds risk clusters, classification models, feature relationships, and model evaluation visuals.",
        "artifacts": [
            "FoodSafety_Malnutrition/data/processed/main_clustered.csv",
            "FoodSafety_Malnutrition/outputs/plots/clusters.png",
            "FoodSafety_Malnutrition/outputs/plots/elbow_curve.png",
            "FoodSafety_Malnutrition/outputs/plots/dendrogram.png",
            "FoodSafety_Malnutrition/outputs/plots/hierarchical_clusters.png",
            "FoodSafety_Malnutrition/outputs/plots/dbscan_clusters.png",
            "FoodSafety_Malnutrition/outputs/plots/k_distance_graph.png",
            "FoodSafety_Malnutrition/outputs/plots/cluster_characteristics.png",
            "FoodSafety_Malnutrition/outputs/plots/feature_correlation.png",
            "FoodSafety_Malnutrition/outputs/plots/confusion_matrix.png",
            "FoodSafety_Malnutrition/outputs/plots/roc_curve.png",
            "FoodSafety_Malnutrition/models/logistic_regression.pkl",
            "FoodSafety_Malnutrition/models/random_forest.pkl",
            "FoodSafety_Malnutrition/models/xgboost.pkl",
            "FoodSafety_Malnutrition/models/label_encoder.pkl",
        ],
    },
    {
        "title": "03 - ANN, BiLSTM & RCNN",
        "notebook": "03_ANN_BiLSTM_RCNN.ipynb",
        "summary": "Adds deep learning models for tabular classification, time-series forecasting, and text-based risk prediction.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/ann_training.png",
            "FoodSafety_Malnutrition/outputs/plots/ann_confusion_matrix.png",
            "FoodSafety_Malnutrition/outputs/plots/bilstm_prediction.png",
            "FoodSafety_Malnutrition/outputs/plots/rcnn_training.png",
            "FoodSafety_Malnutrition/models/ann_model.h5",
            "FoodSafety_Malnutrition/models/bilstm_model.h5",
            "FoodSafety_Malnutrition/models/rcnn_model.h5",
        ],
    },
    {
        "title": "04 - Explainable & Agentic AI",
        "notebook": "04_Explainable_Agentic_AI.ipynb",
        "summary": "Shows model drivers with SHAP and generates country-level risk reports.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/shap_summary_rf.png",
            "FoodSafety_Malnutrition/outputs/plots/shap_importance_xgb.png",
            "FoodSafety_Malnutrition/outputs/reports/country_risk_reports.txt",
        ],
    },
    {
        "title": "05 - Generative AI",
        "notebook": "05_Generative_AI.ipynb",
        "summary": "Uses synthetic data generation to improve class balance and compares real versus generated samples.",
        "artifacts": [
            "FoodSafety_Malnutrition/data/processed/combined_with_synthetic.csv",
            "FoodSafety_Malnutrition/outputs/plots/synthetic_class_balance.png",
            "FoodSafety_Malnutrition/outputs/plots/real_vs_synthetic.png",
        ],
    },
    {
        "title": "06 - CNN Crop Disease",
        "notebook": "06_CNN_CropDisease.ipynb",
        "summary": "Trains the crop disease image classifier used as the visual food-safety signal.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/cnn_training.png",
            "FoodSafety_Malnutrition/models/cnn_model.h5",
        ],
    },
    {
        "title": "07 - Cross-Validation & Ensembles",
        "notebook": "07_Cross_Validation_Ensembles.ipynb",
        "summary": "Compares model families and ensemble-readiness with cross-validation style evaluation outputs.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/model_comparison.png",
        ],
        "expected": [
            "FoodSafety_Malnutrition/outputs/plots/cv_ensemble_comparison.png",
        ],
    },
    {
        "title": "08 - Geospatial Visualization",
        "notebook": "08_Geospatial_Visualization.ipynb",
        "summary": "Adds world maps, regional analysis, India district heatmaps, and an interactive Plotly dashboard.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/world_risk_map.html",
            "FoodSafety_Malnutrition/outputs/plots/interactive_dashboard.html",
            "FoodSafety_Malnutrition/outputs/plots/region_analysis.png",
            "FoodSafety_Malnutrition/outputs/plots/regional_analysis.png",
            "FoodSafety_Malnutrition/outputs/plots/india_district_heatmap.png",
            "FoodSafety_Malnutrition/outputs/plots/continental_risk_distribution.png",
            "FoodSafety_Malnutrition/outputs/plots/critical_risk_countries.png",
            "FoodSafety_Malnutrition/outputs/plots/time_series_trends.png",
        ],
    },
    {
        "title": "09 - Hyperparameter Optimization",
        "notebook": "09_Hyperparameter_Optimization.ipynb",
        "summary": "Tunes classical ML models and saves optimized model artifacts.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/hyperparameter_optimization_results.png",
            "FoodSafety_Malnutrition/models/logistic_regression_tuned.pkl",
            "FoodSafety_Malnutrition/models/random_forest_tuned.pkl",
            "FoodSafety_Malnutrition/models/xgboost_tuned.pkl",
        ],
    },
    {
        "title": "10 - Uncertainty Quantification",
        "notebook": "10_Uncertainty_Quantification.ipynb",
        "summary": "Adds calibrated probabilities, confidence bands, and uncertainty-aware decision support.",
        "artifacts": [
            "FoodSafety_Malnutrition/outputs/plots/uncertainty_quantification.png",
            "FoodSafety_Malnutrition/models/logistic_regression_calibrated.pkl",
            "FoodSafety_Malnutrition/models/ann_mc_dropout.h5",
        ],
    },
    {
        "title": "11 - Transfer Learning CNN",
        "notebook": "11_Transfer_Learning_CNN.ipynb",
        "summary": "Documents the transfer-learning CNN work for crop disease image recognition.",
        "artifacts": [],
        "expected": [
            "FoodSafety_Malnutrition/outputs/plots/transfer_learning_resnet50_training.png",
            "FoodSafety_Malnutrition/models/cnn_resnet50_transfer.h5",
        ],
    },
    {
        "title": "12 - Attention BiLSTM",
        "notebook": "12_Attention_BiLSTM.ipynb",
        "summary": "Documents the attention-enhanced time-series forecasting model.",
        "artifacts": [],
        "expected": [
            "FoodSafety_Malnutrition/outputs/plots/attention_bilstm_results.png",
            "FoodSafety_Malnutrition/models/bilstm_attention.h5",
        ],
    },
    {
        "title": "13 - Advanced CNN",
        "notebook": "13_Advanced_CNN.ipynb",
        "summary": "Documents advanced CNN architecture comparison and production model selection.",
        "artifacts": [],
        "expected": [
            "FoodSafety_Malnutrition/outputs/plots/advanced_cnn_comparison.png",
            "FoodSafety_Malnutrition/models/cnn_best_model_production.h5",
        ],
    },
]

APP_TITLE = "Food Safety & Malnutrition Risk Intelligence"
APP_SUBTITLE = "Global nutrition risk, model outputs, geospatial patterns, and notebook evidence in one workspace."
RISK_ORDER = ['Critical Risk', 'Severe Risk', 'High Risk', 'Moderate Risk', 'Low Risk']
INDICATOR_COLUMNS = ['stunting', 'wasting', 'underweight', 'overweight', 'undernourishment_pct']
FEATURE_COLUMNS = [
    'stunting',
    'wasting',
    'underweight',
    'overweight',
    'stunting_avg',
    'wasting_avg',
    'underweight_avg',
    'undernourishment_pct',
]
PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, Segoe UI, sans-serif", "color": "#172033", "size": 13},
    "title": {"font": {"size": 17, "color": "#172033"}, "x": 0.02, "xanchor": "left"},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    "margin": {"l": 20, "r": 20, "t": 56, "b": 28},
}

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Food Safety & Malnutrition Risk",
    page_icon="FoodSafety_Malnutrition/assets/favicon.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --app-bg: #0f172a;
            --panel-bg: #1e293b;
            --text-main: #e5edf8;
            --text-muted: #94a3b8;
            --border: #334155;
            --accent: #3b82f6;
            --accent-soft: #1e3a8a;
            --green: #10b981;
            --amber: #f59e0b;
            --red: #ef4444;
        }

        html, body, [class*="stApp"] {
            background: var(--app-bg);
            color: var(--text-main);
            font-family: Inter, "Segoe UI", sans-serif;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.5rem;
            max-width: 1480px;
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid #1e293b;
        }

        [data-testid="stSidebar"] * {
            color: #e5edf8;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 8px;
            padding: 0.25rem 0.4rem;
            margin-bottom: 0.1rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .app-shell-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1.5rem;
            padding: 1.15rem 1.25rem;
            margin-bottom: 1rem;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.04);
        }

        .app-title {
            margin: 0;
            color: var(--text-main);
            font-size: 1.55rem;
            font-weight: 750;
            letter-spacing: 0;
        }

        .app-subtitle {
            margin: 0.3rem 0 0 0;
            color: var(--text-muted);
            font-size: 0.94rem;
            line-height: 1.45;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            white-space: nowrap;
            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            color: #166534;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 650;
        }

        .page-kicker {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.15rem;
        }

        .page-title {
            margin: 0;
            color: var(--text-main);
            font-size: 1.45rem;
            font-weight: 750;
            letter-spacing: 0;
        }

        .page-subtitle {
            color: var(--text-muted);
            margin: 0.35rem 0 1rem 0;
            max-width: 840px;
            line-height: 1.45;
        }

        .metric-tile {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            min-height: 112px;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.78rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.3rem;
        }

        .metric-value {
            color: var(--text-main);
            font-size: 1.7rem;
            font-weight: 760;
            line-height: 1.15;
            overflow-wrap: anywhere;
        }

        .metric-note {
            color: var(--text-muted);
            font-size: 0.82rem;
            margin-top: 0.35rem;
            line-height: 1.35;
        }

        .section-card {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
        }

        .section-heading {
            margin: 1rem 0 0.55rem 0;
        }

        .section-heading h3 {
            margin: 0;
            color: var(--text-main);
            font-size: 1.02rem;
            font-weight: 740;
            letter-spacing: 0;
        }

        .section-heading p {
            margin: 0.2rem 0 0 0;
            color: var(--text-muted);
            font-size: 0.86rem;
            line-height: 1.4;
        }

        .notice {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-left: 5px solid var(--accent);
            border-radius: 8px;
            color: var(--text-main);
            padding: 0.75rem 0.9rem;
            margin: 0.55rem 0 0.8rem 0;
            font-size: 0.9rem;
            line-height: 1.45;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.03);
        }

        .notice-warning {
            border-left-color: var(--amber);
            background: #fffbeb;
        }

        .notice-success {
            border-left-color: var(--green);
            background: #ecfdf5;
        }

        .risk-result {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-left: 6px solid var(--accent);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            margin: 0.8rem 0 1rem 0;
        }

        .risk-result strong {
            display: block;
            color: var(--text-main);
            font-size: 1.55rem;
            margin-top: 0.15rem;
        }

        .risk-critical { border-left-color: #8b0000; }
        .risk-severe { border-left-color: #c0392b; }
        .risk-high { border-left-color: #e74c3c; }
        .risk-moderate { border-left-color: #f39c12; }
        .risk-low { border-left-color: #2ecc71; }

        div[data-testid="stMetric"] {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
        }

        [data-testid="stSidebar"] div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.12);
            box-shadow: none;
        }

        [data-testid="stSidebar"] div[data-testid="stMetric"] * {
            color: #e5edf8 !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }

        div[data-testid="stPlotlyChart"] {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.35rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
        }

        div[data-testid="stImage"] {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.55rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.03);
        }

        div[data-testid="stImage"] img {
            border-radius: 6px;
        }

        div[data-testid="stForm"],
        div[data-testid="stExpander"] {
            background: var(--panel-bg);
            border-color: var(--border);
            border-radius: 8px;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--border);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.55rem 0.9rem;
        }

        .stTabs [aria-selected="true"] {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-bottom: 1px solid var(--panel-bg);
        }

        .stButton > button {
            border-radius: 8px;
            font-weight: 700;
            border: 1px solid #1d4ed8;
            background: #2563eb;
            color: #ffffff;
        }

        .stButton > button:hover {
            border-color: #1e40af;
            background: #1d4ed8;
            color: #ffffff;
        }

        #MainMenu, footer {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==================== LOAD DATA & MODELS ====================
@st.cache_resource
def load_models():
    # Prefer calibrated LR if present, otherwise fall back to the base model.
    lr_path = MODELS_DIR / "logistic_regression_calibrated.pkl"
    if not lr_path.exists():
        lr_path = MODELS_DIR / "logistic_regression.pkl"
    with open(lr_path, 'rb') as f:
        lr_model = pickle.load(f)
    with open(MODELS_DIR / "label_encoder.pkl", 'rb') as f:
        le = pickle.load(f)
    return lr_model, le

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_DIR / "processed" / "main_clustered.csv")
    return data

def render_app_header():
    st.markdown(f"""
    <div class="app-shell-header">
        <div>
            <h1 class="app-title">{APP_TITLE}</h1>
            <p class="app-subtitle">{APP_SUBTITLE}</p>
        </div>
        <div class="status-pill">Operational</div>
    </div>
    """, unsafe_allow_html=True)

def page_header(title, subtitle=None, kicker=None):
    kicker_html = f'<div class="page-kicker">{kicker}</div>' if kicker else ""
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    {kicker_html}
    <h2 class="page-title">{title}</h2>
    {subtitle_html}
    """, unsafe_allow_html=True)

def metric_tile(label, value, note=""):
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(f"""
    <div class="metric-tile">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {note_html}
    </div>
    """, unsafe_allow_html=True)

def section_heading(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="section-heading">
        <h3>{title}</h3>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def notice(message, tone="info"):
    class_name = "notice"
    if tone == "warning":
        class_name += " notice-warning"
    elif tone == "success":
        class_name += " notice-success"
    st.markdown(f'<div class="{class_name}">{message}</div>', unsafe_allow_html=True)

def styled_container_open():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

def styled_container_close():
    st.markdown('</div>', unsafe_allow_html=True)

def format_number(value):
    return f"{value:,.0f}"

def format_percent(value):
    return f"{value:.1f}%"

def risk_class_name(risk_label):
    if "Critical" in risk_label:
        return "risk-critical"
    if "Severe" in risk_label:
        return "risk-severe"
    if "High" in risk_label:
        return "risk-high"
    if "Moderate" in risk_label:
        return "risk-moderate"
    return "risk-low"

def style_figure(fig, height=420):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#eef2f7", zeroline=False)
    return fig

def filter_records(df, key_prefix="global"):
    filters = st.container()
    with filters:
        col1, col2, col3 = st.columns([1.2, 1.4, 1.2])
        years = sorted(df["year"].dropna().astype(int).unique()) if "year" in df else []
        regions = sorted(df["region"].dropna().unique()) if "region" in df else []
        risks = [risk for risk in RISK_ORDER if risk in set(df["risk_label"].dropna())]

        if years:
            selected_years = col1.slider(
                "Year range",
                min_value=min(years),
                max_value=max(years),
                value=(min(years), max(years)),
                key=f"{key_prefix}_years",
            )
        else:
            selected_years = None

        selected_regions = col2.multiselect(
            "Regions",
            regions,
            default=regions,
            key=f"{key_prefix}_regions",
        )
        selected_risks = col3.multiselect(
            "Risk levels",
            risks,
            default=risks,
            key=f"{key_prefix}_risks",
        )

    filtered = df.copy()
    if selected_years is not None:
        filtered = filtered[
            (filtered["year"] >= selected_years[0])
            & (filtered["year"] <= selected_years[1])
        ]
    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]
    if selected_risks:
        filtered = filtered[filtered["risk_label"].isin(selected_risks)]
    return filtered

def risk_counts_frame(df):
    counts = df["risk_label"].value_counts().reindex(RISK_ORDER).dropna()
    return counts.rename_axis("Risk Level").reset_index(name="Records")

def country_summary(df):
    return df.groupby("country").agg({
        "stunting": "mean",
        "wasting": "mean",
        "underweight": "mean",
        "overweight": "mean",
        "undernourishment_pct": "mean",
        "risk_label": lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    }).reset_index()

@st.cache_data(ttl=20, show_spinner=False)
def check_api_status():
    try:
        response = requests.get("http://localhost:5000/health", timeout=1.5)
        if response.ok:
            payload = response.json()
            return "Online", payload.get("models_loaded", {})
    except Exception:
        pass
    return "Offline", {}

@st.cache_data(show_spinner=False)
def read_text_artifact(path_str):
    return Path(path_str).read_text(encoding="utf-8", errors="replace")

@st.cache_data(show_spinner=False)
def preview_csv(path_str, rows=20):
    return pd.read_csv(path_str, nrows=rows)

def artifact_path(relative_path):
    return PROJECT_ROOT / relative_path

def relative_to_project(path):
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)

def format_file_size(path):
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def display_name(path):
    return path.stem.replace("_", " ").title()

def classify_artifact(path):
    suffix = path.suffix.lower()
    if suffix in [".png", ".jpg", ".jpeg", ".webp"]:
        return "image"
    if suffix == ".html":
        return "html"
    if suffix in [".txt", ".md"]:
        return "text"
    if suffix in [".csv", ".xlsx", ".xls"]:
        return "table"
    if suffix in [".pkl", ".h5", ".keras", ".joblib"]:
        return "model"
    if suffix == ".ipynb":
        return "notebook"
    return "file"

def file_inventory(paths):
    rows = []
    for path in paths:
        if path.exists():
            rows.append({
                "File": path.name,
                "Type": classify_artifact(path).title(),
                "Size": format_file_size(path),
                "Path": relative_to_project(path),
            })
    return pd.DataFrame(rows)

def collect_notebook_artifacts():
    artifacts = []
    for entry in NOTEBOOK_OUTPUTS:
        for artifact in entry.get("artifacts", []):
            path = artifact_path(artifact)
            if path.exists():
                artifacts.append((entry["title"], path))
    return artifacts

def render_table_preview(path):
    st.markdown(f"**{path.name}**")
    st.caption(f"{relative_to_project(path)} - {format_file_size(path)}")
    if path.suffix.lower() == ".csv":
        try:
            st.dataframe(preview_csv(str(path)), use_container_width=True)
        except Exception as exc:
            notice(f"Could not preview CSV: {exc}", "warning")
    else:
        notice("Preview is available for CSV files. This file is listed as an exported artifact.")

def render_notebook_entry(entry):
    notebook_path = NOTEBOOKS_DIR / entry["notebook"]
    section_heading(entry["title"], entry["summary"])

    if notebook_path.exists():
        notice(f"Source notebook: {relative_to_project(notebook_path)}", "success")
    else:
        notice(f"Source notebook not found: {entry['notebook']}", "warning")

    existing_paths = [
        artifact_path(artifact)
        for artifact in entry.get("artifacts", [])
        if artifact_path(artifact).exists()
    ]

    missing_expected = [
        artifact
        for artifact in entry.get("expected", [])
        if not artifact_path(artifact).exists()
    ]

    if not existing_paths:
        notice("No exported artifacts from this notebook were found in the workspace yet.", "warning")
    else:
        inventory_df = file_inventory(existing_paths)
        st.dataframe(inventory_df, use_container_width=True, hide_index=True)

    grouped = {"image": [], "html": [], "text": [], "table": [], "model": [], "file": []}
    for path in existing_paths:
        grouped.setdefault(classify_artifact(path), []).append(path)

    if grouped["image"]:
        section_heading("Visual Outputs")
        cols = st.columns(2)
        for index, path in enumerate(grouped["image"]):
            with cols[index % 2]:
                st.image(str(path), caption=display_name(path), use_container_width=True)

    if grouped["html"]:
        section_heading("Interactive Outputs")
        selected_html = st.selectbox(
            "Select interactive output",
            grouped["html"],
            format_func=lambda path: path.name,
            key=f"html_{entry['notebook']}",
        )
        with st.spinner(f"Loading {selected_html.name}"):
            components.html(read_text_artifact(str(selected_html)), height=700, scrolling=True)

    if grouped["text"]:
        section_heading("Text Reports")
        for path in grouped["text"]:
            with st.expander(path.name, expanded=True):
                st.text_area(
                    "Report content",
                    read_text_artifact(str(path)),
                    height=320,
                    key=f"text_{entry['notebook']}_{path.name}",
                )

    if grouped["table"]:
        section_heading("Data Outputs")
        for path in grouped["table"]:
            with st.expander(path.name):
                render_table_preview(path)

    if grouped["model"] or grouped["file"]:
        section_heading("Model and File Artifacts")
        st.dataframe(file_inventory(grouped["model"] + grouped["file"]), use_container_width=True, hide_index=True)

    if missing_expected:
        with st.expander("Expected exports not found"):
            st.caption("These are documented outputs for the notebook but are not present in this workspace.")
            for artifact in missing_expected:
                st.write(f"- {artifact}")

def render_plot_gallery():
    plot_files = sorted(PLOTS_DIR.glob("*.png")) if PLOTS_DIR.exists() else []
    if not plot_files:
        notice("No PNG plot outputs were found.", "warning")
        return

    search = st.text_input("Search plot outputs", placeholder="Example: shap, cnn, cluster, map")
    filtered = [
        path for path in plot_files
        if not search or search.lower() in path.name.lower()
    ]

    st.caption(f"Showing {len(filtered)} of {len(plot_files)} exported plot images.")
    cols = st.columns(3)
    for index, path in enumerate(filtered):
        with cols[index % 3]:
            st.image(str(path), caption=display_name(path), use_container_width=True)

def render_interactive_outputs():
    html_files = sorted(PLOTS_DIR.glob("*.html")) if PLOTS_DIR.exists() else []
    if not html_files:
        notice("No interactive HTML outputs were found.", "warning")
        return

    selected_html = st.selectbox(
        "Select interactive notebook output",
        html_files,
        format_func=lambda path: path.name,
        key="global_interactive_html",
    )
    st.caption(f"{relative_to_project(selected_html)} - {format_file_size(selected_html)}")
    with st.spinner(f"Loading {selected_html.name}"):
        components.html(read_text_artifact(str(selected_html)), height=760, scrolling=True)

def render_reports_and_files():
    report_files = sorted(REPORTS_DIR.glob("*")) if REPORTS_DIR.exists() else []
    data_files = sorted((DATA_DIR / "processed").glob("*")) if (DATA_DIR / "processed").exists() else []
    model_files = sorted(MODELS_DIR.glob("*")) if MODELS_DIR.exists() else []

    section_heading("Reports")
    if report_files:
        for path in report_files:
            with st.expander(path.name, expanded=True):
                if classify_artifact(path) == "text":
                    st.text_area(
                        "Report content",
                        read_text_artifact(str(path)),
                        height=300,
                        key=f"report_{path.name}",
                    )
                else:
                    st.write(f"{relative_to_project(path)} - {format_file_size(path)}")
    else:
        notice("No report files found.")

    section_heading("Generated Datasets")
    if data_files:
        st.dataframe(file_inventory(data_files), use_container_width=True, hide_index=True)
    else:
        notice("No processed data files found.")

    section_heading("Saved Models")
    if model_files:
        st.dataframe(file_inventory(model_files), use_container_width=True, hide_index=True)
    else:
        notice("No model files found.")

def render_notebook_outputs_page():
    page_header(
        "Notebook Output Library",
        "Generated figures, interactive maps, datasets, reports, and model files from the research pipeline.",
        "Evidence Library",
    )

    exported_artifacts = collect_notebook_artifacts()
    interactive_count = len(list(PLOTS_DIR.glob("*.html"))) if PLOTS_DIR.exists() else 0
    plot_count = len(list(PLOTS_DIR.glob("*.png"))) if PLOTS_DIR.exists() else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_tile("Notebooks", len(NOTEBOOK_OUTPUTS), "research modules")
    with col2:
        metric_tile("Plot Outputs", plot_count, "exported figures")
    with col3:
        metric_tile("Interactive HTML", interactive_count, "embedded outputs")
    with col4:
        metric_tile("Artifacts Linked", len(exported_artifacts), "available files")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "By Notebook",
        "Plot Gallery",
        "Interactive HTML",
        "Reports & Files",
    ])

    with tab1:
        selected_entry = st.selectbox(
            "Select notebook",
            NOTEBOOK_OUTPUTS,
            format_func=lambda entry: entry["title"],
        )
        render_notebook_entry(selected_entry)

    with tab2:
        render_plot_gallery()

    with tab3:
        render_interactive_outputs()

    with tab4:
        render_reports_and_files()

lr_model, le = load_models()
data = load_data()

# ==================== SIDEBAR ====================
render_app_header()

st.sidebar.markdown("### Risk Intelligence")
st.sidebar.caption("Food safety and malnutrition analytics")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Predictions",
        "Geospatial",
        "Analytics",
        "Explainability",
        "💬 Chatbot",
        "Notebook Outputs",
        "System Status",
    ],
)
st.sidebar.divider()
st.sidebar.metric("Countries", data["country"].nunique())
st.sidebar.metric("Records", format_number(len(data)))
st.sidebar.metric("Year Span", f"{int(data['year'].min())}-{int(data['year'].max())}")

# ==================== PAGE 1: DASHBOARD ====================
if page == "Dashboard":
    page_header(
        "Global Risk Overview",
        "Country-year risk distribution, regional concentration, and indicator trends.",
        "Executive View",
    )

    filtered_data = filter_records(data, key_prefix="overview")
    if filtered_data.empty:
        notice("No records match the selected filters.", "warning")
    else:
        critical_share = (
            filtered_data["risk_label"].isin(["Critical Risk", "Severe Risk"]).mean() * 100
        )
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_tile("Countries", format_number(filtered_data["country"].nunique()), "unique countries in view")
        with col2:
            metric_tile("Records", format_number(len(filtered_data)), "country-year observations")
        with col3:
            metric_tile("Critical or Severe", format_percent(critical_share), "share of selected records")
        with col4:
            metric_tile(
                "Avg Undernourishment",
                format_percent(filtered_data["undernourishment_pct"].mean()),
                "mean population exposure",
            )

        st.divider()

        col1, col2 = st.columns([0.95, 1.25])
        with col1:
            risk_df = risk_counts_frame(filtered_data)
            fig = px.pie(
                risk_df,
                values="Records",
                names="Risk Level",
                hole=0.58,
                title="Risk Distribution",
                color="Risk Level",
                color_discrete_map=RISK_COLOR_MAP,
                category_orders={"Risk Level": RISK_ORDER},
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(style_figure(fig, height=390), use_container_width=True)

        with col2:
            region_risk = (
                filtered_data.groupby(["region", "risk_label"])
                .size()
                .reset_index(name="Records")
            )
            fig = px.bar(
                region_risk,
                x="region",
                y="Records",
                color="risk_label",
                title="Risk Levels by Region",
                barmode="stack",
                color_discrete_map=RISK_COLOR_MAP,
                category_orders={"risk_label": RISK_ORDER},
            )
            fig.update_layout(xaxis_title="", yaxis_title="Records")
            st.plotly_chart(style_figure(fig, height=390), use_container_width=True)

        col1, col2 = st.columns([1.2, 1])
        with col1:
            yearly = (
                filtered_data.groupby("year")[["stunting", "wasting", "underweight"]]
                .mean()
                .reset_index()
                .melt(id_vars="year", var_name="Indicator", value_name="Average")
            )
            fig = px.line(
                yearly,
                x="year",
                y="Average",
                color="Indicator",
                markers=True,
                title="Indicator Trend",
                color_discrete_sequence=["#2563eb", "#0f9f6e", "#d9822b"],
            )
            fig.update_layout(xaxis_title="", yaxis_title="Average %")
            st.plotly_chart(style_figure(fig, height=390), use_container_width=True)

        with col2:
            summary = country_summary(filtered_data)
            summary["risk_rank"] = summary["risk_label"].map({
                "Low Risk": 1,
                "Moderate Risk": 2,
                "High Risk": 3,
                "Severe Risk": 4,
                "Critical Risk": 5,
            })
            top_countries = (
                summary.sort_values(["risk_rank", "undernourishment_pct"], ascending=False)
                .head(12)
                .drop(columns=["risk_rank"])
            )
            section_heading("Priority Countries", "Countries with the highest current risk concentration in the selected view.")
            st.dataframe(
                top_countries.rename(columns={
                    "country": "Country",
                    "risk_label": "Risk",
                    "stunting": "Stunting",
                    "wasting": "Wasting",
                    "underweight": "Underweight",
                    "overweight": "Overweight",
                    "undernourishment_pct": "Undernourishment",
                }),
                use_container_width=True,
                hide_index=True,
            )

# ==================== PAGE 2: PREDICTIONS ====================
elif page == "Predictions":
    page_header(
        "Risk Prediction Workbench",
        "Adjust malnutrition indicators and inspect class probabilities from the calibrated model.",
        "Model Inference",
    )

    reference_options = ["Global median"] + sorted(data["country"].dropna().unique())
    reference = st.selectbox("Baseline profile", reference_options)
    if reference == "Global median":
        defaults = data[FEATURE_COLUMNS].median()
    else:
        defaults = data[data["country"] == reference].sort_values("year").iloc[-1][FEATURE_COLUMNS]

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            stunting = st.slider("Stunting %", 0.0, 100.0, float(defaults["stunting"]), 0.1)
            wasting = st.slider("Wasting %", 0.0, 100.0, float(defaults["wasting"]), 0.1)
            underweight = st.slider("Underweight %", 0.0, 100.0, float(defaults["underweight"]), 0.1)
            overweight = st.slider("Overweight %", 0.0, 100.0, float(defaults["overweight"]), 0.1)

        with col2:
            stunting_avg = st.slider("Country Avg Stunting %", 0.0, 100.0, float(defaults["stunting_avg"]), 0.1)
            wasting_avg = st.slider("Country Avg Wasting %", 0.0, 100.0, float(defaults["wasting_avg"]), 0.1)
            underweight_avg = st.slider("Country Avg Underweight %", 0.0, 100.0, float(defaults["underweight_avg"]), 0.1)
            undernourishment_pct = st.slider("Undernourishment %", 0.0, 100.0, float(defaults["undernourishment_pct"]), 0.1)

        submitted = st.form_submit_button("Predict risk level")

    if submitted:
        features_array = np.array([[
            stunting,
            wasting,
            underweight,
            overweight,
            stunting_avg,
            wasting_avg,
            underweight_avg,
            undernourishment_pct,
        ]])

        probas = lr_model.predict_proba(features_array)[0]
        pred_class = np.argmax(probas)
        confidence = probas[pred_class]
        risk_label = le.classes_[pred_class]

        st.markdown(f"""
        <div class="risk-result {risk_class_name(risk_label)}">
            <div class="metric-label">Predicted Risk Level</div>
            <strong>{risk_label}</strong>
            <div class="metric-note">Confidence {confidence * 100:.1f}% | prediction score {confidence:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            metric_tile("Model", "Calibrated LR", "probability-calibrated classifier")
        with col2:
            metric_tile("Confidence", format_percent(confidence * 100), "highest class probability")
        with col3:
            metric_tile("Top Class", risk_label, "selected risk label")

        prob_df = pd.DataFrame({
            "Risk Level": le.classes_,
            "Probability": probas,
        }).sort_values("Probability", ascending=False)

        fig = px.bar(
            prob_df,
            x="Probability",
            y="Risk Level",
            orientation="h",
            title="Predicted Probability Distribution",
            color="Risk Level",
            color_discrete_map=RISK_COLOR_MAP,
            category_orders={"Risk Level": RISK_ORDER},
        )
        fig.update_layout(xaxis_tickformat=".0%", xaxis_title="", yaxis_title="")
        st.plotly_chart(style_figure(fig, height=380), use_container_width=True)

# ==================== PAGE 3: GEOSPATIAL ====================
elif page == "Geospatial":
    page_header(
        "Geospatial Risk Map",
        "Country-level map and regional table for malnutrition indicators.",
        "Spatial View",
    )

    country_data = country_summary(data)
    country_data["risk_numeric"] = country_data["risk_label"].map({
        "Low Risk": 1,
        "Moderate Risk": 2,
        "High Risk": 3,
        "Severe Risk": 4,
        "Critical Risk": 5,
    })

    col1, col2 = st.columns([1, 1])
    with col1:
        map_metric = st.selectbox(
            "Map layer",
            ["Risk level", "stunting", "wasting", "underweight", "overweight", "undernourishment_pct"],
        )
    with col2:
        country_filter = st.multiselect(
            "Risk levels",
            [risk for risk in RISK_ORDER if risk in set(country_data["risk_label"])],
            default=[risk for risk in RISK_ORDER if risk in set(country_data["risk_label"])],
            key="map_risk_filter",
        )

    country_data_filtered = country_data[country_data["risk_label"].isin(country_filter)]

    if map_metric == "Risk level":
        fig = px.choropleth(
            country_data_filtered,
            locations="country",
            locationmode="country names",
            color="risk_label",
            hover_name="country",
            hover_data={
                "stunting": ":.1f",
                "wasting": ":.1f",
                "underweight": ":.1f",
                "undernourishment_pct": ":.1f",
                "risk_label": True,
            },
            color_discrete_map=RISK_COLOR_MAP,
            category_orders={"risk_label": RISK_ORDER},
            title="Global Risk Classification",
        )
    else:
        fig = px.choropleth(
            country_data_filtered,
            locations="country",
            locationmode="country names",
            color=map_metric,
            hover_name="country",
            hover_data={map_metric: ":.1f", "risk_label": True},
            color_continuous_scale="YlOrRd",
            title=f"Global {display_name(Path(map_metric))} Rates",
        )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        legend=dict(orientation="h", y=-0.05),
        margin=dict(l=0, r=0, t=48, b=0),
        height=620,
    )
    st.plotly_chart(fig, use_container_width=True)

    section_heading("Country Detail", "Aggregated country indicators and dominant risk level.")
    st.dataframe(
        country_data_filtered.sort_values(["risk_numeric", "undernourishment_pct"], ascending=False)
        .drop(columns=["risk_numeric"])
        .rename(columns={
            "country": "Country",
            "risk_label": "Risk",
            "stunting": "Stunting",
            "wasting": "Wasting",
            "underweight": "Underweight",
            "overweight": "Overweight",
            "undernourishment_pct": "Undernourishment",
        }),
        use_container_width=True,
        hide_index=True,
    )

# ==================== PAGE 4: ANALYTICS ====================
elif page == "Analytics":
    page_header(
        "Analytics & Trends",
        "Longitudinal indicator movement, regional comparison, and feature relationships.",
        "Analytical View",
    )

    filtered_data = filter_records(data, key_prefix="analytics")
    if filtered_data.empty:
        notice("No records match the selected filters.", "warning")
    else:
        tab1, tab2, tab3 = st.tabs(["Trends", "Regional Comparison", "Relationships"])

        with tab1:
            yearly = (
                filtered_data.groupby("year")[INDICATOR_COLUMNS]
                .mean()
                .reset_index()
                .melt(id_vars="year", var_name="Indicator", value_name="Average")
            )
            fig = px.line(
                yearly,
                x="year",
                y="Average",
                color="Indicator",
                markers=True,
                title="Global Indicator Trend",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(xaxis_title="", yaxis_title="Average %")
            st.plotly_chart(style_figure(fig, height=470), use_container_width=True)

        with tab2:
            region_stats = (
                filtered_data.groupby("region")[["stunting", "wasting", "underweight", "undernourishment_pct"]]
                .mean()
                .reset_index()
                .melt(id_vars="region", var_name="Indicator", value_name="Average")
            )
            fig = px.bar(
                region_stats,
                x="region",
                y="Average",
                color="Indicator",
                barmode="group",
                title="Regional Indicator Comparison",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(xaxis_title="", yaxis_title="Average %")
            st.plotly_chart(style_figure(fig, height=470), use_container_width=True)

        with tab3:
            corr_matrix = filtered_data[FEATURE_COLUMNS].corr()
            fig = px.imshow(
                corr_matrix,
                labels=dict(color="Correlation"),
                x=FEATURE_COLUMNS,
                y=FEATURE_COLUMNS,
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Feature Correlation Matrix",
            )
            st.plotly_chart(style_figure(fig, height=620), use_container_width=True)

# ==================== PAGE 5: EXPLAINABILITY ====================
elif page == "Explainability":
    page_header(
        "Model Explainability",
        "Feature-level drivers from the explainability notebooks and production model summary.",
        "Model Trust",
    )

    features = ['Underweight', 'Overweight', 'Undernourishment', 'Stunting', 'Wasting']
    importance = [1.26, 1.15, 1.07, 0.98, 0.88]
    drivers = pd.DataFrame({"Feature": features, "SHAP Value": importance})

    col1, col2 = st.columns([1.15, 0.85])
    with col1:
        fig = px.bar(
            drivers.sort_values("SHAP Value"),
            x="SHAP Value",
            y="Feature",
            orientation="h",
            title="Feature Importance",
            color="SHAP Value",
            color_continuous_scale="Blues",
        )
        fig.update_layout(xaxis_title="Mean absolute SHAP value", yaxis_title="")
        st.plotly_chart(style_figure(fig, height=420), use_container_width=True)

    with col2:
        section_heading("Top Drivers", "Ranked drivers currently surfaced in the explainability notebook outputs.")
        st.dataframe(drivers, use_container_width=True, hide_index=True)
        col_a, col_b = st.columns(2)
        with col_a:
            metric_tile("Primary Driver", "Underweight", "highest SHAP contribution")
        with col_b:
            metric_tile("Model Family", "Classical ML", "LR, RF, and XGBoost outputs")

    shap_paths = [
        PLOTS_DIR / "shap_summary_rf.png",
        PLOTS_DIR / "shap_importance_xgb.png",
    ]
    available_shap = [path for path in shap_paths if path.exists()]
    if available_shap:
        section_heading("Notebook SHAP Outputs", "Exported SHAP figures from the explainability workflow.")
        cols = st.columns(len(available_shap))
        for index, path in enumerate(available_shap):
            with cols[index]:
                st.image(str(path), caption=display_name(path), use_container_width=True)

# ==================== PAGE 6: CHATBOT ====================
elif page == "💬 Chatbot":
    page_header(
        "AI Chatbot Assistant",
        "Ask questions about food safety & nutrition. Get instant predictions powered by Groq.",
        "Interactive AI",
    )

    # Initialize chatbot in session state
    if "chatbot" not in st.session_state:
        try:
            # Lazy import to avoid errors if groq is not installed
            from groq_chatbot import FoodSafetyChatbot
            from models_loader import ModelsLoader
            from predict_engine import PredictionEngine

            groq_api_key = os.getenv('GROQ_API_KEY')
            if groq_api_key:
                models_loader = ModelsLoader()
                models_loader.load_all_models()
                prediction_engine = PredictionEngine(models_loader)
                st.session_state.chatbot = FoodSafetyChatbot(groq_api_key, prediction_engine)
                st.session_state.chat_ready = True
            else:
                st.session_state.chat_ready = False
                st.error("⚠️ GROQ_API_KEY environment variable not set. Please configure your Groq API key.")
        except Exception as e:
            st.session_state.chat_ready = False
            st.error(f"❌ Error initializing chatbot: {str(e)}")

    if st.session_state.chat_ready:
        # Initialize chat messages
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input
        st.divider()
        user_input = st.chat_input("Ask about food safety, nutrition risks, or predictions...")

        if user_input:
            # Add user message to history
            st.session_state.chat_messages.append({"role": "user", "content": user_input})

            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = st.session_state.chatbot.chat(user_input)
                        st.markdown(response)
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})

        # Sidebar options
        st.sidebar.divider()
        if st.sidebar.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.chat_messages = []
            if st.session_state.chat_ready:
                st.session_state.chatbot.reset_conversation()
            st.rerun()

        # Help section
        with st.sidebar.expander("💡 Chatbot Help"):
            st.markdown("""
            **What can I do?**
            - Answer questions about food safety and nutrition
            - Make risk predictions from metrics
            - Explain which factors drive predictions
            - Provide policy recommendations

            **Example Prompts:**
            - "What is stunting?"
            - "Predict risk for Kenya with 35% stunting, 18% wasting..."
            - "What are the top risk factors?"
            - "How does malnutrition affect development?"
            """)

# ==================== PAGE 7: NOTEBOOK OUTPUTS ====================
elif page == "Notebook Outputs":
    render_notebook_outputs_page()

# ==================== PAGE 8: SYSTEM STATUS ====================
elif page == "System Status":
    page_header(
        "System Status",
        "Runtime checks, artifact inventory, and model performance summary.",
        "Operations",
    )

    api_status, api_models = check_api_status()
    model_files = list(MODELS_DIR.glob("*")) if MODELS_DIR.exists() else []
    data_files = list((DATA_DIR / "processed").glob("*")) if (DATA_DIR / "processed").exists() else []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_tile("Dashboard", "Online", "Streamlit is serving this app")
    with col2:
        metric_tile("API", api_status, "localhost:5000 health check")
    with col3:
        metric_tile("Model Files", len(model_files), "saved artifacts")
    with col4:
        metric_tile("Data Files", len(data_files), "processed datasets")

    st.divider()

    performance_data = {
        "Model": ["Logistic Regression", "Random Forest", "XGBoost", "ANN", "BiLSTM", "RCNN", "CNN"],
        "Accuracy": [0.9788, 0.9048, 0.9048, 0.9206, 0.933, 0.9275, 0.8327],
        "Type": ["Classification"] * 3 + ["Deep Learning"] * 4,
    }

    perf_df = pd.DataFrame(performance_data)
    col1, col2 = st.columns([1.15, 0.85])
    with col1:
        fig = px.bar(
            perf_df,
            x="Model",
            y="Accuracy",
            color="Type",
            title="Model Performance Comparison",
            color_discrete_map={"Classification": "#2563eb", "Deep Learning": "#0f9f6e"},
        )
        fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Accuracy")
        st.plotly_chart(style_figure(fig, height=430), use_container_width=True)

    with col2:
        section_heading("API Model Status")
        if api_models:
            model_status_df = pd.DataFrame(
                [{"Model": name, "Status": status} for name, status in api_models.items()]
            )
            st.dataframe(model_status_df, use_container_width=True, hide_index=True)
        else:
            notice("API model status is available when the Flask service is running.")

    section_heading("Deployment Commands")
    st.code("""python -m streamlit run streamlit_app.py --server.port=8501
python FoodSafety_Malnutrition/api/app.py
docker-compose up -d""", language="bash")

# ==================== FOOTER ====================
st.divider()
st.caption("Food Safety & Malnutrition Risk Intelligence | Critical, severe, high, moderate, and low risk classes use a consistent severity color scale.")
