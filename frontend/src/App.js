import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import HomePage from './components/HomePage';
import ContribuintePage from './components/ContribuintePage';
import WorkInProgressPage from './components/WorkInProgressPage';
import DarfPage from './components/DarfPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/contribuinte" element={<ContribuintePage />} />
          <Route path="/e-financeira" element={<WorkInProgressPage title="e-Financeira" />} />
          <Route path="/darf" element={<DarfPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
