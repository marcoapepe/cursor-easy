import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './UploadPage.css';

function UploadPage() {
  const navigate = useNavigate();
  const [selectedModule, setSelectedModule] = useState('A'); // Default to Module A
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000';

  const handleFileSelect = (file) => {
    if (file && (file.name.endsWith('.csv') || file.name.endsWith('.txt'))) {
      setSelectedFile(file);
      setError('');
      setUploadResult(null);
    } else {
      setError('Please select a valid CSV or TXT file');
      setSelectedFile(null);
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleModuleChange = (e) => {
    setSelectedModule(e.target.value);
    // Clear results when module changes
    setUploadResult(null);
    setError('');
  };

  const processFile = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setIsProcessing(true);
    setError('');
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(
        `${API_BASE_URL}/contribuinte/bulk-upload?module=${selectedModule}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setUploadResult(response.data);
    } catch (err) {
      console.error('Error processing file:', err);
      setError(err.response?.data?.detail || 'Error processing file');
    } finally {
      setIsProcessing(false);
    }
  };

  const clearResults = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <div className="page-header">
          <div className="page-header-left">
            <button 
              className="back-button"
              onClick={() => navigate('/')}
            >
              ← Back to Home
            </button>
            <h1>Upload - File Upload</h1>
          </div>
          <div className="module-selector">
            <label htmlFor="module-select">Module:</label>
            <select
              id="module-select"
              value={selectedModule}
              onChange={handleModuleChange}
              className="module-select"
            >
              <option value="A">Module A</option>
              <option value="B">Module B</option>
            </select>
          </div>
        </div>

        <div className="upload-section">
          <div className="upload-info">
            <h2>Upload Contribuinte Records</h2>
            <p>Upload a CSV or TXT file with contribuinte records to <strong>Module {selectedModule}</strong> in the following format:</p>
            <div className="format-example">
              <code>dat_proce;cpf_cnpj;cliente;email;dat_cadastro</code>
            </div>
            <div className="format-details">
              <p><strong>Example:</strong></p>
              <code>2025-07-06;77845896512;Rodrigo Pepe;rodrigo@uol.com.br;2025-06-02</code>
            </div>
          </div>

          <div className="upload-actions">
            <div 
              className={`upload-area ${isDragOver ? 'drag-over' : ''} ${selectedFile ? 'has-file' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={handleUploadClick}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv,.txt"
                onChange={handleFileInputChange}
                style={{ display: 'none' }}
              />
              
              {selectedFile ? (
                <div className="file-info">
                  <div className="file-icon">📄</div>
                  <div className="file-details">
                    <div className="file-name">{selectedFile.name}</div>
                    <div className="file-size">{formatFileSize(selectedFile.size)}</div>
                  </div>
                  <button 
                    className="remove-file"
                    onClick={(e) => {
                      e.stopPropagation();
                      clearResults();
                    }}
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <div className="upload-placeholder">
                  <div className="upload-icon">📁</div>
                  <div className="upload-text">
                    <strong>Click to upload</strong> or drag and drop
                  </div>
                  <div className="upload-hint">CSV or TXT files only</div>
                </div>
              )}
            </div>

            <div className="action-buttons">
              <button
                className="upload-btn"
                onClick={handleUploadClick}
                disabled={isProcessing}
              >
                📁 Select File
              </button>
              
              <button
                className="process-btn"
                onClick={processFile}
                disabled={!selectedFile || isProcessing}
              >
                {isProcessing ? '⏳ Processing...' : '⚡ Process File'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {uploadResult && (
          <div className="result-section">
            <div className={`result-card ${uploadResult.error_count > 0 ? 'has-errors' : 'success'}`}>
              <h3>Upload Results for Module {selectedModule}</h3>
              
              <div className="result-stats">
                <div className="stat-item success">
                  <span className="stat-label">Successfully Processed:</span>
                  <span className="stat-value">{uploadResult.success_count}</span>
                </div>
                
                {uploadResult.error_count > 0 && (
                  <div className="stat-item error">
                    <span className="stat-label">Errors:</span>
                    <span className="stat-value">{uploadResult.error_count}</span>
                  </div>
                )}
              </div>

              {uploadResult.errors && uploadResult.errors.length > 0 && (
                <div className="error-details">
                  <h4>Error Details:</h4>
                  <div className="error-list">
                    {uploadResult.errors.map((error, index) => (
                      <div key={index} className="error-item">
                        {error}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <button 
                className="clear-btn"
                onClick={clearResults}
              >
                Upload Another File
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadPage; 