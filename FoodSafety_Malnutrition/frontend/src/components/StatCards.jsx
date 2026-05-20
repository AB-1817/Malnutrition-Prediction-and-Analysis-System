import React from 'react';
import { Users, TrendingUp, AlertTriangle, Globe } from 'lucide-react';

export default function StatCards({ summaryData }) {
  if (!summaryData) return null;

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-title">
          <Globe size={16} color="var(--chart-blue)" />
          Global Avg Stunting
        </div>
        <div className="stat-value">{summaryData.globalAvgStunting}%</div>
        <div style={{fontSize: '12px', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', gap: '4px'}}>
          <TrendingUp size={12} /> Model Input
        </div>
      </div>
      
      <div className="stat-card">
        <div className="stat-title">
          <Users size={16} color="var(--chart-purple)" />
          Districts Analyzed
        </div>
        <div className="stat-value">{summaryData.totalDistricts}</div>
        <div style={{fontSize: '12px', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', gap: '4px'}}>
          <TrendingUp size={12} /> India Dataset
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-title">
          <AlertTriangle size={16} color="var(--chart-orange)" />
          Avg FSI Score
        </div>
        <div className="stat-value">{summaryData.avgFSIScore}</div>
        <div style={{fontSize: '12px', color: 'var(--chart-orange)', display: 'flex', alignItems: 'center', gap: '4px'}}>
           Risk Indicator
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-title">
          <AlertTriangle size={16} color="#ef4444" />
          Critical Risk Zones
        </div>
        <div className="stat-value">{summaryData.criticalHighRiskZones}</div>
        <div style={{fontSize: '12px', color: '#ef4444', display: 'flex', alignItems: 'center', gap: '4px'}}>
          High Priority Districts
        </div>
      </div>
    </div>
  );
}
