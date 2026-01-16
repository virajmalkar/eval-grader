import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export default function EvaluationProgress() {
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRunId, setSelectedRunId] = useState(null);
  const [runDetails, setRunDetails] = useState(null);

  useEffect(() => {
    fetchEvaluations();
    const interval = setInterval(fetchEvaluations, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchEvaluations = async () => {
    try {
      const response = await apiClient.listEvaluations(0, 50);
      setEvaluations(response.data || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectRun = async (runId) => {
    setSelectedRunId(runId);
    try {
      const response = await apiClient.getEvaluationResults(runId);
      setRunDetails(response.data);
    } catch (err) {
      setError(err.message);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      pending: 'status-pending',
      running: 'status-running',
      completed: 'status-completed',
      failed: 'status-failed',
    };
    return statusMap[status] || 'status-unknown';
  };

  if (loading) return <div className="loading">Loading evaluations...</div>;

  return (
    <div className="evaluation-progress">
      <h2>Evaluation Progress</h2>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="progress-container">
        <div className="runs-list">
          <h3>Recent Runs</h3>
          {evaluations.length === 0 ? (
            <p className="text-muted">No evaluations yet</p>
          ) : (
            <div className="runs-table">
              {evaluations.map((run) => (
                <div
                  key={run.id}
                  className={`run-item ${selectedRunId === run.id ? 'selected' : ''}`}
                  onClick={() => handleSelectRun(run.id)}
                >
                  <div className="run-header">
                    <span className={`status-badge ${getStatusBadge(run.status)}`}>
                      {run.status}
                    </span>
                    <code className="run-id">{run.id.substring(0, 8)}...</code>
                  </div>
                  <div className="run-info">
                    <small>Test Cases: {run.test_case_ids.length}</small>
                    <small>Results: {run.result_count}</small>
                    {run.started_at && (
                      <small>Started: {new Date(run.started_at).toLocaleTimeString()}</small>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {runDetails && selectedRunId && (
          <div className="run-details">
            <h3>Results for {selectedRunId.substring(0, 8)}...</h3>
            
            {runDetails.summary && (
              <div className="summary-stats">
                <div className="stat">
                  <span className="stat-label">Total:</span>
                  <span className="stat-value">{runDetails.summary.total}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Successful:</span>
                  <span className="stat-value success">{runDetails.summary.successful}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Failed:</span>
                  <span className="stat-value error">{runDetails.summary.failed}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Timeout:</span>
                  <span className="stat-value warning">{runDetails.summary.timeout}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Avg Latency:</span>
                  <span className="stat-value">{runDetails.summary.avg_latency_ms}ms</span>
                </div>
              </div>
            )}

            {runDetails.results && (
              <div className="results-list">
                <h4>Results ({runDetails.results.length})</h4>
                <div className="results-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Test Case</th>
                        <th>Status</th>
                        <th>Response</th>
                        <th>Latency</th>
                      </tr>
                    </thead>
                    <tbody>
                      {runDetails.results.map((result) => (
                        <tr key={result.id}>
                          <td className="test-id">{result.test_case_id.substring(0, 8)}...</td>
                          <td>
                            <span className={`badge ${result.response_status}`}>
                              {result.response_status}
                            </span>
                          </td>
                          <td className="response">
                            {result.response_status === 'success'
                              ? (result.agent_response?.substring(0, 50) || '-')
                              : (result.error_message?.substring(0, 50) || '-')}
                          </td>
                          <td>{result.response_latency_ms || '-'}ms</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
