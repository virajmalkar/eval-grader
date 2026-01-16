import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import GraderSelector from './GraderSelector';

export default function EvaluationRunner() {
  const [testCases, setTestCases] = useState([]);
  const [formData, setFormData] = useState({
    test_case_ids: [],
    agent_endpoint_url: 'http://localhost:9000/evaluate',
    grader_ids: ['string-match'],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    fetchTestCases();
  }, []);

  const fetchTestCases = async () => {
    try {
      const response = await apiClient.listTestCases(0, 100);
      setTestCases(response.data || []);
    } catch (err) {
      setError(`Failed to load test cases: ${err.message}`);
    }
  };

  const handleTestCaseToggle = (testCaseId) => {
    setFormData((prev) => ({
      ...prev,
      test_case_ids: prev.test_case_ids.includes(testCaseId)
        ? prev.test_case_ids.filter((id) => id !== testCaseId)
        : [...prev.test_case_ids, testCaseId],
    }));
  };

  const handleUrlChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      agent_endpoint_url: e.target.value,
    }));
  };

  const handleGradersChange = (graderIds) => {
    setFormData((prev) => ({
      ...prev,
      grader_ids: graderIds,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.test_case_ids.length === 0) {
      setError('Please select at least one test case');
      return;
    }

    if (!formData.agent_endpoint_url.trim()) {
      setError('Please enter agent endpoint URL');
      return;
    }

    try {
      setLoading(true);
      await apiClient.createEvaluation(formData);
      setSuccess('Evaluation started! Check progress in the Status tab.');
      setTimeout(() => setSuccess(null), 3000);
      setFormData({
        test_case_ids: [],
        agent_endpoint_url: 'http://localhost:9000/evaluate',
        grader_ids: ['string-match'],
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="evaluation-runner">
      <h2>Run Evaluation</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="runner-form">
        <div className="form-group">
          <label>Agent Endpoint URL *</label>
          <input
            type="url"
            value={formData.agent_endpoint_url}
            onChange={handleUrlChange}
            placeholder="http://localhost:9000/evaluate"
            required
          />
        </div>

        <div className="form-group">
          <label>Select Test Cases * ({formData.test_case_ids.length} selected)</label>
          <div className="checkbox-group">
            {testCases.length === 0 ? (
              <p className="text-muted">No test cases available. Create some first!</p>
            ) : (
              testCases.map((tc) => (
                <label key={tc.id} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={formData.test_case_ids.includes(tc.id)}
                    onChange={() => handleTestCaseToggle(tc.id)}
                  />
                  <span>{tc.input.substring(0, 60)}...</span>
                </label>
              ))
            )}
          </div>
        </div>

        <GraderSelector
          selectedGraders={formData.grader_ids}
          onGradersChange={handleGradersChange}
        />

        <button
          type="submit"
          disabled={loading || testCases.length === 0}
          className="btn-primary"
        >
          {loading ? 'Starting...' : 'Start Evaluation'}
        </button>
      </form>

      <div className="runner-help">
        <h3>Tips</h3>
        <ul>
          <li>Default: Uses mock agent at http://localhost:9000/evaluate</li>
          <li>Run <code>python mock_agent_server.py</code> to start the mock agent</li>
          <li>Select test cases and graders, then click Start</li>
          <li>Evaluation runs in the background</li>
        </ul>
      </div>
    </div>
  );
}
