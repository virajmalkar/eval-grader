import { useState, useEffect } from 'react';
import TestCaseForm from '../components/TestCaseForm';
import TestCaseList from '../components/TestCaseList';
import { apiClient } from '../services/api';

export default function TestCaseManager() {
  const [mode, setMode] = useState('list'); // 'list' or 'create'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleCreateTestCase = async (formData) => {
    try {
      setLoading(true);
      await apiClient.createTestCase(formData);
      setSuccess('Test case created successfully!');
      setMode('list');
      setTimeout(() => setSuccess(null), 3000);
      // Trigger refresh
      window.location.reload();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="test-case-manager">
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="manager-controls">
        <button
          onClick={() => setMode('list')}
          className={`btn ${mode === 'list' ? 'btn-primary' : 'btn-secondary'}`}
        >
          View All
        </button>
        <button
          onClick={() => setMode('create')}
          className={`btn ${mode === 'create' ? 'btn-primary' : 'btn-secondary'}`}
        >
          Create New
        </button>
      </div>

      <div className="manager-content">
        {mode === 'list' && <TestCaseList />}
        {mode === 'create' && (
          <TestCaseForm onSubmit={handleCreateTestCase} isLoading={loading} />
        )}
      </div>
    </div>
  );
}
