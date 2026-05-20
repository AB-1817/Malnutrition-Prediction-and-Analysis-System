import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import StatCards from '../components/StatCards';
import Charts from '../components/Charts';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/dashboard_data.json')
      .then(res => res.json())
      .then(data => {
        setDashboardData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading dashboard data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="main-content">
      <Header title="Executive Summary" />
      <div className="content-wrapper">
        {loading ? (
          <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px'}}>
            <p style={{color: 'var(--text-secondary)'}}>Loading dashboard metrics...</p>
          </div>
        ) : (
          <>
            <StatCards summaryData={dashboardData?.summaryCards} />
            <Charts chartsData={dashboardData?.charts} />
          </>
        )}
      </div>
    </div>
  );
}
