import React, { useState } from 'react';
import Header from '../components/Header';

export default function RiskModels() {
  const [activeTab, setActiveTab] = useState('Explainability');
  
  const tabs = ['Explainability', 'Deep Learning', 'Classification', 'Clustering', 'Generative AI'];
  
  const categories = {
    'Explainability': [
      { id: 'shap_summary_rf.png', label: 'Global SHAP Summary' },
      { id: 'shap_importance_xgb.png', label: 'XGBoost Feature Importance' },
      { id: 'india_feature_importance.png', label: 'India Features (Agentic AI)' }
    ],
    'Deep Learning': [
      { id: 'india_lstm_training_curves.png', label: 'LSTM Training Curves' },
      { id: 'india_lstm_forecast.png', label: 'LSTM Time Series Forecast' },
      { id: 'india_ann_training_curves.png', label: 'ANN India Training' },
      { id: 'cnn_training.png', label: 'CNN Crop Disease Training' }
    ],
    'Classification': [
      { id: 'india_model_comparison.png', label: 'Model Performance Comparison' },
      { id: 'india_confusion_matrices.png', label: 'Confusion Matrices' },
      { id: 'india_ann_confusion_matrix.png', label: 'ANN Confusion Matrix' },
      { id: 'roc_curve.png', label: 'Global ROC Curve' }
    ],
    'Clustering': [
      { id: 'india_cluster_visualization.png', label: 'District Cluster Visualization' },
      { id: 'india_kmeans_elbow.png', label: 'K-Means Elbow Method' },
      { id: 'india_hierarchical_dendrogram.png', label: 'Hierarchical Dendrogram' },
      { id: 'dbscan_clusters.png', label: 'DBSCAN Global' }
    ],
    'Generative AI': [
      { id: 'real_vs_synthetic.png', label: 'Real vs Synthetic Data' },
      { id: 'synthetic_class_balance.png', label: 'Class Balancing with CTGAN' }
    ]
  };

  return (
    <div className="main-content">
      <Header title="Risk Models & ML Evaluation" />
      
      <div className="content-wrapper">
        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '8px 16px',
                border: 'none',
                backgroundColor: 'transparent',
                color: activeTab === tab ? 'var(--color-primary)' : 'var(--text-secondary)',
                borderBottom: activeTab === tab ? '2px solid var(--color-primary)' : '2px solid transparent',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '14px',
                marginBottom: '-13px'
              }}
            >
              {tab}
            </button>
          ))}
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
          {categories[activeTab].map(img => (
            <div key={img.id} className="chart-card" style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
              <h3 className="chart-title">{img.label}</h3>
              <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#fafafa', borderRadius: '8px', padding: '16px' }}>
                <img 
                  src={`/assets/${img.id}`} 
                  alt={img.label} 
                  style={{ maxWidth: '100%', maxHeight: '400px', objectFit: 'contain' }}
                  onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'block'; }}
                />
                <p style={{display: 'none', color: 'var(--text-secondary)'}}>Image not available</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
