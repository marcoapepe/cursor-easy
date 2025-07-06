import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  const handleOptionClick = (path) => {
    navigate(path);
  };

  return (
    <div className="home-page">
      <div className="home-container">
        <h1 className="project-title">Easy Interfaces</h1>
        
        <div className="options-grid">
          <div 
            className="option-card"
            onClick={() => handleOptionClick('/contribuinte')}
          >
            <div className="option-icon">👤</div>
            <h2>Contribuinte</h2>
            <p>Manage contribuinte records</p>
          </div>
          
          <div 
            className="option-card"
            onClick={() => handleOptionClick('/e-financeira')}
          >
            <div className="option-icon">💰</div>
            <h2>e-Financeira</h2>
            <p>Financial management system</p>
          </div>
          
          <div 
            className="option-card"
            onClick={() => handleOptionClick('/darf')}
          >
            <div className="option-icon">📄</div>
            <h2>DARF</h2>
            <p>DARF document management</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage; 