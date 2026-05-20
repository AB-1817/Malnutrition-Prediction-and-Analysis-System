import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Geospatial from './pages/Geospatial';
import RiskModels from './pages/RiskModels';
import Reports from './pages/Reports';
import './index.css';

export default function App() {
  return (
    <Router>
      <div className="dashboard-layout">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/geospatial" element={<Geospatial />} />
          <Route path="/models" element={<RiskModels />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </div>
    </Router>
  );
}
