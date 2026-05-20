import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, ComposedChart, Line
} from 'recharts';

const COLORS = ['#8b5cf6', '#3b82f6', '#0ea5e9', '#10b981', '#f59e0b', '#ef4444'];

export default function Charts({ chartsData }) {
  if (!chartsData) return null;

  return (
    <>
      <div className="charts-grid">
        <div className="chart-card">
          <div className="chart-header">
            <h2 className="chart-title">Production Output vs Rainfall (1997-2014)</h2>
            <div className="chart-legend">
              <div className="legend-item"><div className="legend-dot" style={{backgroundColor: 'var(--chart-blue)'}}></div> Kharif</div>
              <div className="legend-item"><div className="legend-dot" style={{backgroundColor: 'var(--chart-orange)'}}></div> Rabi</div>
              <div className="legend-item"><div className="legend-dot" style={{backgroundColor: 'var(--chart-teal)'}}></div> Rainfall</div>
            </div>
          </div>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <ComposedChart data={chartsData.productionByYear} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                <XAxis dataKey="year" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <Tooltip cursor={{fill: 'var(--bg-app)'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: 'var(--shadow-md)'}} />
                <Bar yAxisId="left" dataKey="Kharif" stackId="a" fill="var(--chart-blue)" radius={[0, 0, 4, 4]} barSize={20} />
                <Bar yAxisId="left" dataKey="Rabi" stackId="a" fill="var(--chart-orange)" radius={[4, 4, 0, 0]} barSize={20} />
                <Line yAxisId="right" type="monotone" dataKey="Rainfall" stroke="var(--chart-teal)" strokeWidth={3} dot={{r: 4, fill: 'var(--chart-teal)', strokeWidth: 0}} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-header">
            <h2 className="chart-title">District Risk Distribution</h2>
          </div>
          <div style={{ width: '100%', height: 300, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <ResponsiveContainer width="100%" height="80%">
              <PieChart>
                <Pie
                  data={chartsData.riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {chartsData.riskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: 'var(--shadow-md)'}} />
              </PieChart>
            </ResponsiveContainer>
            
            <div style={{display: 'flex', flexWrap: 'wrap', gap: '12px', justifyContent: 'center', marginTop: '16px'}}>
               {chartsData.riskDistribution.map((entry, index) => (
                  <div key={index} className="legend-item" style={{fontSize: '11px'}}>
                    <div className="legend-dot" style={{backgroundColor: COLORS[index % COLORS.length]}}></div>
                    {entry.name} - {entry.value}
                  </div>
               ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bottom-charts">
        <div className="chart-card">
          <div className="chart-header">
            <h2 className="chart-title">High-Risk Districts by State</h2>
          </div>
          <div style={{ width: '100%', height: 250 }}>
            <ResponsiveContainer>
              <BarChart layout="vertical" data={chartsData.riskByState} margin={{ top: 0, right: 30, left: 30, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border-color)" />
                <XAxis type="number" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <YAxis type="category" dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <Tooltip cursor={{fill: 'var(--bg-app)'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: 'var(--shadow-md)'}} />
                <Bar dataKey="FSI_Score" fill="var(--color-primary)" radius={[0, 4, 4, 0]} barSize={12} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="chart-card">
          <div className="chart-header">
            <h2 className="chart-title">Global Undernourishment by Region</h2>
          </div>
          <div style={{ width: '100%', height: 250 }}>
            <ResponsiveContainer>
              <BarChart layout="vertical" data={chartsData.globalRegionRisk} margin={{ top: 0, right: 30, left: 30, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border-color)" />
                <XAxis type="number" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <YAxis type="category" dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <Tooltip cursor={{fill: 'var(--bg-app)'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: 'var(--shadow-md)'}} />
                <Bar dataKey="Undernourishment" fill="var(--chart-teal)" radius={[0, 4, 4, 0]} barSize={12} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </>
  );
}
