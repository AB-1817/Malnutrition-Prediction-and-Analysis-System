# Food Safety & Malnutrition Interactive Dashboard

## Overview
This interactive dashboard provides comprehensive visualizations and insights from the Food Safety & Malnutrition Prediction System project. It integrates outputs from all project notebooks into a single, user-friendly interface.

## Features

### 🏠 Overview Page
- Key statistics and metrics
- Global coverage information
- Quick insights into malnutrition indicators

### 📊 Data Exploration
- **Distribution Analysis**: Histograms and box plots of malnutrition indicators
- **Correlation Analysis**: Heatmaps and scatter plot matrices
- **Time Series**: Trend analysis for individual countries

### 🎯 Clustering Analysis
- Risk group distribution (Low, Moderate, High, Severe, Critical)
- Cluster characteristics and profiles
- 3D visualization of risk clusters
- Interactive radar charts

### 🤖 Predictions
- **Single Prediction**: Interactive sliders to input indicators and get real-time predictions
- **Batch Predictions**: Upload CSV files for bulk predictions
- Multiple model comparisons (Logistic Regression, Random Forest, XGBoost)
- Confidence scores and probability distributions

### 📈 Model Performance
- Comparative analysis of all models
- Performance metrics (Accuracy, Precision, Recall, F1-Score)
- Interactive visualizations

### 🗺️ Geospatial Analysis
- Interactive world maps showing malnutrition indicators
- Regional analysis and comparisons
- Country-level details

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
# Navigate to the project directory
cd FoodSafety_Malnutrition

# Install dashboard requirements
pip install -r dashboard_requirements.txt
```

### Step 2: Verify Data Files
Ensure the following data files exist:
- `data/processed/main_merged.csv`
- `data/processed/india_district.csv`

### Step 3: Verify Model Files
Ensure trained models exist in the `models/` directory:
- `logistic_regression_calibrated.pkl`
- `random_forest_tuned.pkl`
- `xgboost_tuned.pkl`
- `label_encoder.pkl`

## Running the Dashboard

### Method 1: Using Streamlit Command
```bash
# From the FoodSafety_Malnutrition directory
streamlit run dashboard.py
```

### Method 2: Using Python
```bash
python -m streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## Usage Guide

### Navigation
- Use the sidebar to navigate between different pages
- Each page has multiple tabs for detailed analysis
- Interactive elements include sliders, dropdowns, and file uploaders

### Making Predictions
1. Go to the "🤖 Predictions" page
2. Use the "Make Prediction" tab for single predictions
3. Adjust sliders to input malnutrition indicators
4. Click "Predict Risk Level" to see results from all models
5. For batch predictions, upload a CSV file with the required columns

### Required CSV Format for Batch Predictions
Your CSV file should contain the following columns:
- stunting
- wasting
- underweight
- overweight
- stunting_avg
- wasting_avg
- underweight_avg
- undernourishment_pct

Example:
```csv
stunting,wasting,underweight,overweight,stunting_avg,wasting_avg,underweight_avg,undernourishment_pct
25.5,10.2,20.1,5.3,23.0,9.0,18.0,15.0
30.0,12.5,25.0,4.5,28.0,11.0,22.0,18.0
```

### Exploring Data
1. Navigate to "📊 Data Exploration"
2. Switch between tabs to view different analyses
3. Use dropdowns to select specific countries or variables
4. Hover over charts for detailed information

### Viewing Clusters
1. Go to "🎯 Clustering Analysis"
2. Explore the distribution of risk groups
3. View cluster characteristics in the heatmap
4. Select specific clusters to see detailed profiles
5. Interact with the 3D visualization

### Geospatial Analysis
1. Navigate to "🗺️ Geospatial Analysis"
2. Select an indicator from the dropdown
3. Hover over countries to see specific values
4. Scroll down for regional comparisons

## Troubleshooting

### Dashboard won't start
- Ensure all dependencies are installed: `pip install -r dashboard_requirements.txt`
- Check Python version: `python --version` (should be 3.10+)
- Verify you're in the correct directory

### Data not loading
- Check that `data/processed/main_merged.csv` exists
- Verify file permissions
- Check the console for specific error messages

### Models not loading
- Ensure model files exist in the `models/` directory
- Check that pickle files are not corrupted
- Verify you've run the training notebooks first

### Port already in use
If port 8501 is already in use, specify a different port:
```bash
streamlit run dashboard.py --server.port 8502
```

## Customization

### Changing Colors
Edit the color schemes in the dashboard.py file:
- Look for `color_discrete_sequence` parameters
- Modify `color_continuous_scale` for heatmaps

### Adding New Visualizations
1. Create a new function in dashboard.py
2. Add it to the appropriate page function
3. Use Plotly Express or Plotly Graph Objects for consistency

### Modifying Layout
- Adjust column ratios in `st.columns([1, 2])` calls
- Change chart heights with `height` parameter
- Modify the sidebar content in the `main()` function

## Performance Tips

### For Large Datasets
- The dashboard uses `@st.cache_data` for data loading
- Models are cached with `@st.cache_resource`
- Clear cache if data is updated: Click "Clear cache" in the hamburger menu

### Optimizing Load Times
- Reduce the number of data points in visualizations
- Use data sampling for very large datasets
- Consider pre-computing expensive calculations

## Project Structure
```
FoodSafety_Malnutrition/
├── dashboard.py                 # Main dashboard application
├── dashboard_requirements.txt   # Dashboard dependencies
├── data/
│   └── processed/
│       ├── main_merged.csv     # Main dataset
│       └── india_district.csv  # India district data
├── models/                      # Trained models
│   ├── logistic_regression_calibrated.pkl
│   ├── random_forest_tuned.pkl
│   ├── xgboost_tuned.pkl
│   └── label_encoder.pkl
└── outputs/                     # Generated outputs
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Ensure all prerequisites are met
4. Verify data and model files are present

## Credits

This dashboard integrates work from multiple notebooks:
- 01_Data_Collection_Merging.ipynb
- 02_Clustering_Classification.ipynb
- 03_ANN_BiLSTM_RCNN.ipynb
- 07_Cross_Validation_Ensembles.ipynb
- 08_Geospatial_Visualization.ipynb
- 09_Hyperparameter_Optimization.ipynb

## License

This project is part of the Food Safety & Malnutrition Prediction System.
