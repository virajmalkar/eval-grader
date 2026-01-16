/**
 * Frontend API client for backend communication
 */

const API_BASE_URL = '/api';

class APIClient {
  async request(method, endpoint, data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  }

  // Test Cases API
  async createTestCase(testCaseData) {
    return this.request('POST', '/test-cases', testCaseData);
  }

  async getTestCase(id) {
    return this.request('GET', `/test-cases/${id}`);
  }

  async listTestCases(skip = 0, limit = 10) {
    return this.request('GET', `/test-cases?skip=${skip}&limit=${limit}`);
  }

  async updateTestCase(id, data) {
    return this.request('PUT', `/test-cases/${id}`, data);
  }

  async deleteTestCase(id) {
    return this.request('DELETE', `/test-cases/${id}`);
  }

  // Evaluations API
  async createEvaluation(runData) {
    return this.request('POST', '/evaluations', runData);
  }

  async getEvaluationStatus(id) {
    return this.request('GET', `/evaluations/${id}`);
  }

  async listEvaluations(skip = 0, limit = 10) {
    return this.request('GET', `/evaluations?skip=${skip}&limit=${limit}`);
  }

  async getEvaluationResults(id) {
    return this.request('GET', `/evaluations/${id}/results`);
  }

  // Graders API
  async listGraders() {
    return this.request('GET', '/graders');
  }

  async getGrader(id) {
    return this.request('GET', `/graders/${id}`);
  }

  // Health check
  async healthCheck() {
    return this.request('GET', '/health');
  }
}

export const apiClient = new APIClient();
