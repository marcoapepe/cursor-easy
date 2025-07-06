import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';
import './ContribuintePage.css';

function ContribuintePage() {
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState('');
  const [cpfCnpj, setCpfCnpj] = useState('');
  const [clientName, setClientName] = useState('');
  const [contribuintes, setContribuintes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE_URL = 'http://localhost:8000';

  const clearOtherFilters = (activeFilter) => {
    if (activeFilter !== 'date') setSelectedDate('');
    if (activeFilter !== 'cpf') setCpfCnpj('');
    if (activeFilter !== 'client') setClientName('');
  };

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

  const fetchContribuinteByCpf = async (cpf) => {
    if (!cpf) {
      setContribuintes([]);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`${API_BASE_URL}/contribuinte/cpf/${cpf}`);
      // Convert single result to array for consistency
      setContribuintes([response.data]);
    } catch (err) {
      console.error('Error fetching contribuinte by CPF:', err);
      if (err.response?.status === 404) {
        setError('CPF/CNPJ not found');
      } else {
        setError(err.response?.data?.detail || 'Error fetching data');
      }
      setContribuintes([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchContribuintesByClient = async (client) => {
    if (!client) {
      setContribuintes([]);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`${API_BASE_URL}/contribuinte/by-client/${client}`);
      setContribuintes(response.data);
    } catch (err) {
      console.error('Error fetching contribuintes by client:', err);
      setError(err.response?.data?.detail || 'Error fetching data');
      setContribuintes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDateChange = (e) => {
    const date = e.target.value;
    setSelectedDate(date);
    clearOtherFilters('date');
    fetchContribuintesByDate(date);
  };

  const handleCpfCnpjChange = (e) => {
    const cpf = e.target.value;
    setCpfCnpj(cpf);
    clearOtherFilters('cpf');
    fetchContribuinteByCpf(cpf);
  };

  const handleClientNameChange = (e) => {
    const client = e.target.value;
    setClientName(client);
    clearOtherFilters('client');
    fetchContribuintesByClient(client);
  };

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'dd/MM/yyyy');
    } catch {
      return dateString;
    }
  };

  const getActiveFilter = () => {
    if (selectedDate) return 'date';
    if (cpfCnpj) return 'cpf';
    if (clientName) return 'client';
    return null;
  };

  const getFilterDisplayText = () => {
    const activeFilter = getActiveFilter();
    if (activeFilter === 'date') return `Date: ${formatDate(selectedDate)}`;
    if (activeFilter === 'cpf') return `CPF/CNPJ: ${cpfCnpj}`;
    if (activeFilter === 'client') return `Client: ${clientName}`;
    return null;
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

        <div className="filters-section">
          <div className="filter-row">
            <div className="filter-group">
              <label htmlFor="date-picker">Process Date:</label>
              <input
                id="date-picker"
                type="date"
                value={selectedDate}
                onChange={handleDateChange}
                className="filter-input"
                placeholder="Select date"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="cpf-cnpj">CPF/CNPJ:</label>
              <input
                id="cpf-cnpj"
                type="text"
                value={cpfCnpj}
                onChange={handleCpfCnpjChange}
                className="filter-input"
                placeholder="Enter CPF or CNPJ"
                maxLength="14"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="client-name">Client Name:</label>
              <input
                id="client-name"
                type="text"
                value={clientName}
                onChange={handleClientNameChange}
                className="filter-input"
                placeholder="Enter client name"
                maxLength="80"
              />
            </div>
          </div>
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
              Found {contribuintes.length} record(s) for {getFilterDisplayText()}
            </div>
          ) : (selectedDate || cpfCnpj || clientName) && !loading ? (
            <div className="no-results">
              No records found for {getFilterDisplayText()}
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