import React, { useState } from 'react';
import Header from '../components/Header';

export default function Geospatial() {
  const [activeMap, setActiveMap] = useState('india_district_risk_map.html');
  
  const maps = [
    { id: 'india_district_risk_map.html', name: 'District Risk Map' },
    { id: 'india_fsi_interactive_map.html', name: 'Interactive FSI Map' },
    { id: 'world_risk_map.html', name: 'World Risk Map' },
    { id: 'india_cluster_map.html', name: 'Cluster Visualization' },
    { id: 'india_crop_diversity_map.html', name: 'Crop Diversity Map' },
    { id: 'india_state_production_map.html', name: 'State Production Map' }
  ];

  return (
    <div className="main-content">
      <Header title="Geospatial Intelligence" />
      
      <div className="content-wrapper" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', flexWrap: 'wrap' }}>
          {maps.map(m => (
            <button
              key={m.id}
              onClick={() => setActiveMap(m.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                border: activeMap === m.id ? 'none' : '1px solid var(--border-color)',
                backgroundColor: activeMap === m.id ? 'var(--color-primary)' : 'var(--bg-surface)',
                color: activeMap === m.id ? 'white' : 'var(--text-secondary)',
                cursor: 'pointer',
                fontWeight: 500,
                fontSize: '13px',
                boxShadow: activeMap === m.id ? '0 2px 4px rgba(0, 184, 124, 0.2)' : 'none',
                transition: 'all 0.2s'
              }}
            >
              {m.name}
            </button>
          ))}
        </div>
        
        <div className="chart-card" style={{ flex: 1, display: 'flex', padding: 0, overflow: 'hidden' }}>
          <iframe 
            src={`/assets/${activeMap}`} 
            style={{ width: '100%', height: '100%', border: 'none', minHeight: '600px' }}
            title="Geospatial Map"
          />
        </div>
      </div>
    </div>
  );
}
