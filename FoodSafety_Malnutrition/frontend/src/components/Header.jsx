import React from 'react';
import { Calendar } from 'lucide-react';

export default function Header({ title = "Dashboard" }) {
  return (
    <div className="header">
      <h1>{title}</h1>
      <div style={{
        display: 'flex', 
        alignItems: 'center', 
        gap: '8px', 
        backgroundColor: 'var(--bg-surface)', 
        padding: '8px 16px',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        fontSize: '14px',
        color: 'var(--text-secondary)'
      }}>
        <Calendar size={16} />
        <span>Time period: 1997 - 2014</span>
      </div>
    </div>
  );
}
