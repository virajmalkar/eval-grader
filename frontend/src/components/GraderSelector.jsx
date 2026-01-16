import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export default function GraderSelector({ selectedGraders, onGradersChange }) {
  const [graders, setGraders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGraders();
  }, []);

  const fetchGraders = async () => {
    try {
      const response = await apiClient.listGraders();
      setGraders(response.data || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = (graderId) => {
    const updated = selectedGraders.includes(graderId)
      ? selectedGraders.filter((id) => id !== graderId)
      : [...selectedGraders, graderId];
    onGradersChange(updated);
  };

  if (loading) return <div className="loading">Loading graders...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="grader-selector">
      <h3>Select Graders ({selectedGraders.length} selected)</h3>
      <div className="graders-grid">
        {graders.map((grader) => (
          <div
            key={grader.id}
            className={`grader-card ${selectedGraders.includes(grader.id) ? 'selected' : ''}`}
            onClick={() => handleToggle(grader.id)}
          >
            <div className="grader-header">
              <input
                type="checkbox"
                checked={selectedGraders.includes(grader.id)}
                onChange={() => handleToggle(grader.id)}
                onClick={(e) => e.stopPropagation()}
              />
              <h4>{grader.name}</h4>
            </div>
            <p className="grader-description">{grader.description}</p>
            <div className="grader-config">
              {grader.config && Object.entries(grader.config).length > 0 && (
                <>
                  <small>Config:</small>
                  <ul>
                    {Object.entries(grader.config).map(([key, value]) => (
                      <li key={key}>
                        <code>{key}</code>: {String(value)}
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
