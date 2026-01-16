import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export default function TestCaseList() {
  const [testCases, setTestCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchTestCases();
  }, []);

  const fetchTestCases = async () => {
    try {
      setLoading(true);
      const response = await apiClient.listTestCases(0, 100);
      setTestCases(response.data || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this test case?')) return;
    
    try {
      await apiClient.deleteTestCase(id);
      setTestCases(testCases.filter(tc => tc.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div className="loading">Loading test cases...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="test-case-list">
      <div className="list-header">
        <h2>Test Cases ({testCases.length})</h2>
      </div>

      {testCases.length === 0 ? (
        <div className="empty-state">
          <p>No test cases yet. Create one to get started!</p>
        </div>
      ) : (
        <div className="test-cases-table">
          <table>
            <thead>
              <tr>
                <th>Input</th>
                <th>Expected Output</th>
                <th>Description</th>
                <th>Tags</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {testCases.map((tc) => (
                <tr key={tc.id} className={selectedId === tc.id ? 'selected' : ''}>
                  <td className="input-cell">{tc.input.substring(0, 50)}...</td>
                  <td className="output-cell">{tc.expected_output.substring(0, 50)}...</td>
                  <td>{tc.description || '-'}</td>
                  <td>
                    {tc.tags?.length > 0 ? (
                      <div className="tags-display">
                        {tc.tags.map((tag) => (
                          <span key={tag} className="tag-small">
                            {tag}
                          </span>
                        ))}
                      </div>
                    ) : (
                      '-'
                    )}
                  </td>
                  <td>
                    <button
                      onClick={() => setSelectedId(tc.id)}
                      className="btn-small"
                    >
                      View
                    </button>
                    <button
                      onClick={() => handleDelete(tc.id)}
                      className="btn-small btn-danger"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
