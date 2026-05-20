import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Map, TrendingUp, FileText, Settings, LogOut, Sprout } from 'lucide-react';

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <Sprout size={28} />
        <span>AgriRisk</span>
      </div>
      
      <div className="sidebar-nav">
        <p style={{fontSize: '11px', color: 'var(--text-secondary)', padding: '0 12px', marginTop: '16px', marginBottom: '8px', fontWeight: 600}}>ANALYTICS</p>
        <NavLink to="/" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")} end>
          <LayoutDashboard size={18} /> Dashboard
        </NavLink>
        <NavLink to="/geospatial" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
          <Map size={18} /> Geospatial
        </NavLink>
        <NavLink to="/models" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
          <TrendingUp size={18} /> Risk Models
        </NavLink>
        <NavLink to="/reports" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
          <FileText size={18} /> Reports
        </NavLink>
        
        <p style={{fontSize: '11px', color: 'var(--text-secondary)', padding: '0 12px', marginTop: '24px', marginBottom: '8px', fontWeight: 600}}>SYSTEM</p>
        <a className="nav-item"><Settings size={18} /> Settings</a>
      </div>
      
      <div style={{marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '16px'}}>
        <a className="nav-item"><LogOut size={18} /> Log out</a>
      </div>
    </div>
  );
}
