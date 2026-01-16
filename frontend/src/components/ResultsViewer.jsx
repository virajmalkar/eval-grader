import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export default function ResultsViewer() {
  const [evaluations, setEvaluations] = useState([]);
  const [selectedRun, setSelectedRun] = useState(null);
  const [runDetails, setRunDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchEvaluations();
    const interval = setInterval(fetchEvaluations, 3000);
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

  const handleSelectRun = async (run) => {
    setSelectedRun(run);
    try {
      const response = await apiClient.getEvaluationResults(run.id);
      setRunDetails(response.data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleExportJSON = () => {
    if (!runDetails) return;
    const data = JSON.stringify(runDetails, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `results-${selectedRun.id.substring(0, 8)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleExportCSV = () => {
    if (!runDetails || !runDetails.results) return;
    
    const headers = ['Result ID', 'Test Case ID', 'Agent Response', 'Status', 'Latency (ms)', 'Scores'];
    const rows = runDetails.results.map((r) => [
      r.id.substring(0, 8),
      r.test_case_id.substring(0, 8),
      r.agent_response?.substring(0, 50) || '-',
      r.response_status,
      r.response_latency_ms || '-',
      r.scores?.length || 0,
    ]);

    const csv = [
      headers.join(','),
      ...rows.map((r) => r.map((v) => `"${v}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `results-${selectedRun.id.substring(0, 8)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getFilteredResults = () => {
    if (!runDetails || !runDetails.results) return [];
    if (filterStatus === 'all') return runDetails.results;
    return runDetails.results.filter((r) => r.response_status === filterStatus);
  };

  if (loading) return <div className="loading">Loading results...</div>;

  const filteredResults = getFilteredResults();

  return (
    <div className="results-viewer">
      <h2>Evaluation Results</h2>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="results-layout">
        <div className="runs-sidebar">
          <h3>Recent Evaluations</h3>
          <div className="runs-list">
            {evaluations.length === 0 ? (
              <p className="text-muted">No evaluations yet</p>
            ) : (
              evaluations.map((run) => (
                <div
                  key={run.id}
                  className={`run-card ${selectedRun?.id === run.id ? 'selected' : ''}`}
                  onClick={() => handleSelectRun(run)}
                >
                  <div className="run-status-badge" title={run.status}>
                    {run.status.charAt(0).toUpperCase()}
                  </div>
                  <div className="run-info">
                    <small className="run-id">{run.id.substring(0, 12)}...</small>
                    <small>{run.result_count} results</small>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {selectedRun && runDetails && (
          <div className="results-main">
            <div className="results-header">
              <h3>Results: {selectedRun.id.substring(0, 12)}...</h3>
              <div className="export-buttons">
                <button onClick={handleExportJSON} className="btn-secondary btn-small">
                  Export JSON
                </button>
                <button onClick={handleExportCSV} className="btn-secondary btn-small">
                  Export CSV
                </button>
              </div>
            </div>

            {runDetails.summary && (
              <div className="results-summary">
                <div className="summary-item">
                  <span className="summary-label">Total Results</span>
                  <span className="summary-value">{runDetails.summary.total}</span>
                </div>
                <div className="summary-item success">
                  <span className="summary-label">Successful</span>
                  <span className="summary-value">{runDetails.summary.successful}</span>
                </div>
                <div className="summary-item error">
                  <span className="summary-label">Failed</span>
                  <span className="summary-value">{runDetails.summary.failed}</span>
                </div>
                <div className="summary-item warning">
                  <span className="summary-label">Timeout</span>
                  <span className="summary-value">{runDetails.summary.timeout}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Avg Latency</span>
                  <span className="summary-value">{runDetails.summary.avg_latency_ms}ms</span>
                </div>
              </div>
            )}

            <div className="results-filter">
              <label>Filter by Status:</label>
              <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
                <option value="all">All ({runDetails.results.length})</option>
                <option value="success">Successful ({runDetails.results.filter(r => r.response_status === 'success').length})</option>
                <option value="error">Error ({runDetails.results.filter(r => r.response_status === 'error').length})</option>
                <option value="timeout">Timeout ({runDetails.results.filter(r => r.response_status === 'timeout').length})</option>
              </select>
            </div>

            <div className="results-table-wrapper">
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Test Case</th>
                    <th>Agent Response</th>
                    <th>Status</th>
                    <th>Latency</th>
                    <th>Scores</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredResults.map((result) => (
                    <tr key={result.id}>
                      <td className="code">{result.test_case_id.substring(0, 8)}</td>
                      <td className="response">
                        {result.response_status === 'success'
                          ? (result.agent_response?.substring(0, 40) || '-')
                          : (result.error_message?.substring(0, 40) || '-')}
                      </td>
                      <td>
                        <span className={`badge ${result.response_status}`}>
                          {result.response_status}
                        </span>
                      </td>
                      <td>{result.response_latency_ms || '-'}ms</td>
                      <td>
                        {result.scores && result.scores.length > 0 ? (
                          <span className="score-count">
                            {result.scores.filter(s => s.passed).length}/{result.scores.length} ✓
                          </span>
                        ) : (
                          '-'
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {!selectedRun && (
          <div className="results-empty">
            <p>Select an evaluation to view detailed results</p>
          </div>
        )}
      </div>
    </div>
  );
}
