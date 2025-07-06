import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';
import './ContribuintePage.css';

function ContribuintePage() {
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState('');
  const [contribuintes, setContribuintes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE_URL = 'http://localhost:8000';

  const fetchContribuintesByDate = async (date) => {
    if (!date) {
      setContribuintes([]);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`${API_BASE_URL}/contribuinte/by-date/${date}`);
      setContribuintes(response.data);
    } catch (err) {
      console.error('Error fetching contribuintes:', err);
      setError(err.response?.data?.detail || 'Error fetching data');
      setContribuintes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDateChange = (e) => {
    const date = e.target.value;
    setSelectedDate(date);
    fetchContribuintesByDate(date);
  };

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'dd/MM/yyyy');
    } catch {
      return dateString;
    }
  };

  return (
    <div className="contribuinte-page">
      <div className="contribuinte-container">
        <div className="page-header">
          <button 
            className="back-button"
            onClick={() => navigate('/')}
          >
            ← Back to Home
          </button>
          <h1>Contribuinte Management</h1>
        </div>

        <div className="date-filter-section">
          <label htmlFor="date-picker">Select Process Date:</label>
          <input
            id="date-picker"
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            className="date-input"
          />
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            Loading...
          </div>
        )}

        <div className="results-section">
          {contribuintes.length > 0 ? (
            <div className="results-info">
              Found {contribuintes.length} record(s) for {formatDate(selectedDate)}
            </div>
          ) : selectedDate && !loading ? (
            <div className="no-results">
              No records found for {formatDate(selectedDate)}
            </div>
          ) : null}
        </div>

        {contribuintes.length > 0 && (
          <div className="table-container">
            <table className="contribuinte-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Process Date</th>
                  <th>CPF/CNPJ</th>
                  <th>Client</th>
                  <th>Email</th>
                  <th>Registration Date</th>
                </tr>
              </thead>
              <tbody>
                {contribuintes.map((contribuinte) => (
                  <tr key={contribuinte.ref_id}>
                    <td>{contribuinte.ref_id}</td>
                    <td>{formatDate(contribuinte.dat_proce)}</td>
                    <td>{contribuinte.cpf_cnpj}</td>
                    <td>{contribuinte.cliente}</td>
                    <td>{contribuinte.email || '-'}</td>
                    <td>{contribuinte.dat_cadastro ? formatDate(contribuinte.dat_cadastro) : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default ContribuintePage; 