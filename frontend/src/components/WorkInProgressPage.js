import React from 'react';
import { useNavigate } from 'react-router-dom';
import './WorkInProgressPage.css';

function WorkInProgressPage({ title }) {
  const navigate = useNavigate();

  return (
    <div className="work-in-progress-page">
      <div className="work-container">
        <div className="work-icon">🚧</div>
        <h1>{title}</h1>
        <p className="work-message">Working in progress...</p>
        <button 
          className="back-button"
          onClick={() => navigate('/')}
        >
          ← Back to Home
        </button>
      </div>
    </div>
  );
}

export default WorkInProgressPage; 