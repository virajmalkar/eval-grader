import { useState } from 'react';

export default function TestCaseForm({ onSubmit, initialValues, isLoading }) {
  const [formData, setFormData] = useState(
    initialValues || {
      input: '',
      expected_output: '',
      description: '',
      tags: [],
    }
  );
  const [tagInput, setTagInput] = useState('');
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData((prev) => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()],
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tag) => {
    setFormData((prev) => ({
      ...prev,
      tags: prev.tags.filter((t) => t !== tag),
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.input.trim()) newErrors.input = 'Input is required';
    if (!formData.expected_output.trim()) newErrors.expected_output = 'Expected output is required';
    if (formData.input.length > 10000) newErrors.input = 'Input must be less than 10000 characters';
    if (formData.expected_output.length > 10000) newErrors.expected_output = 'Expected output must be less than 10000 characters';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="test-case-form">
      <div className="form-group">
        <label htmlFor="input">Input *</label>
        <textarea
          id="input"
          name="input"
          value={formData.input}
          onChange={handleChange}
          placeholder="Enter the input to send to the agent"
          rows={4}
          className={errors.input ? 'input-error' : ''}
        />
        {errors.input && <span className="error-message">{errors.input}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="expected_output">Expected Output *</label>
        <textarea
          id="expected_output"
          name="expected_output"
          value={formData.expected_output}
          onChange={handleChange}
          placeholder="Enter the expected response"
          rows={4}
          className={errors.expected_output ? 'input-error' : ''}
        />
        {errors.expected_output && <span className="error-message">{errors.expected_output}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Optional description of this test case"
          rows={3}
        />
      </div>

      <div className="form-group">
        <label htmlFor="tagInput">Tags</label>
        <div className="tag-input-group">
          <input
            type="text"
            id="tagInput"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            placeholder="Add a tag and press enter or click add"
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
          />
          <button type="button" onClick={handleAddTag} className="btn-secondary">
            Add Tag
          </button>
        </div>
        <div className="tags-display">
          {formData.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
              <button type="button" onClick={() => handleRemoveTag(tag)}>
                ✕
              </button>
            </span>
          ))}
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" disabled={isLoading} className="btn-primary">
          {isLoading ? 'Saving...' : 'Save Test Case'}
        </button>
      </div>
    </form>
  );
}
