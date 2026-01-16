import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResultsViewer from './ResultsViewer';
import * as apiClient from '../services/api';

vi.mock('../services/api');

describe('ResultsViewer', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    apiClient.apiClient.listEvaluations.mockImplementation(() => 
      new Promise(() => {}) // Never resolves
    );
    
    render(<ResultsViewer />);
    expect(screen.getByText(/Loading results/i)).toBeInTheDocument();
  });

  it('displays error message on fetch failure', async () => {
    apiClient.apiClient.listEvaluations.mockRejectedValue(
      new Error('API Error')
    );

    render(<ResultsViewer />);
    
    await waitFor(() => {
      expect(screen.getByText(/API Error/i)).toBeInTheDocument();
    });
  });

  it('displays list of evaluations', async () => {
    const mockEvaluations = [
      { id: '123abc', status: 'completed', result_count: 5 },
      { id: '456def', status: 'pending', result_count: 0 },
    ];

    apiClient.apiClient.listEvaluations.mockResolvedValue({
      data: mockEvaluations,
    });

    render(<ResultsViewer />);

    await waitFor(() => {
      expect(screen.getByText('123abc...')).toBeInTheDocument();
      expect(screen.getByText('456def...')).toBeInTheDocument();
    });
  });

  it('selects evaluation and fetches results', async () => {
    const mockEvaluations = [
      { id: '123abc', status: 'completed', result_count: 5 },
    ];

    const mockResults = {
      summary: {
        total: 5,
        successful: 4,
        failed: 1,
        timeout: 0,
        avg_latency_ms: 145,
      },
      results: [
        {
          id: 'r1',
          test_case_id: 'tc1',
          agent_response: 'Hello',
          response_status: 'success',
          response_latency_ms: 150,
          scores: [{ passed: true }],
        },
      ],
    };

    apiClient.apiClient.listEvaluations.mockResolvedValue({
      data: mockEvaluations,
    });

    apiClient.apiClient.getEvaluationResults.mockResolvedValue({
      data: mockResults,
    });

    render(<ResultsViewer />);

    await waitFor(() => {
      expect(screen.getByText('123abc...')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('123abc...'));

    await waitFor(() => {
      expect(apiClient.apiClient.getEvaluationResults).toHaveBeenCalledWith('123abc');
      expect(screen.getByText('Results: 123abc...')).toBeInTheDocument();
    });
  });

  it('filters results by status', async () => {
    const mockEvaluations = [
      { id: '123abc', status: 'completed', result_count: 3 },
    ];

    const mockResults = {
      summary: {
        total: 3,
        successful: 2,
        failed: 1,
        timeout: 0,
        avg_latency_ms: 140,
      },
      results: [
        {
          id: 'r1',
          test_case_id: 'tc1',
          agent_response: 'Hello',
          response_status: 'success',
          response_latency_ms: 130,
          scores: [{ passed: true }],
        },
        {
          id: 'r2',
          test_case_id: 'tc2',
          agent_response: 'World',
          response_status: 'success',
          response_latency_ms: 150,
          scores: [{ passed: true }],
        },
        {
          id: 'r3',
          test_case_id: 'tc3',
          agent_response: null,
          response_status: 'error',
          response_latency_ms: 140,
          error_message: 'Agent failed',
          scores: [],
        },
      ],
    };

    apiClient.apiClient.listEvaluations.mockResolvedValue({
      data: mockEvaluations,
    });

    apiClient.apiClient.getEvaluationResults.mockResolvedValue({
      data: mockResults,
    });

    const { container } = render(<ResultsViewer />);

    await waitFor(() => {
      expect(screen.getByText('123abc...')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('123abc...'));

    await waitFor(() => {
      const select = container.querySelector('.results-filter select');
      fireEvent.change(select, { target: { value: 'error' } });
    });

    await waitFor(() => {
      // Should show only error result
      const rows = container.querySelectorAll('.results-table tbody tr');
      expect(rows.length).toBe(1);
    });
  });

  it('exports results as JSON', async () => {
    const mockEvaluations = [
      { id: '123abc', status: 'completed', result_count: 1 },
    ];

    const mockResults = {
      summary: {
        total: 1,
        successful: 1,
        failed: 0,
        timeout: 0,
        avg_latency_ms: 100,
      },
      results: [
        {
          id: 'r1',
          test_case_id: 'tc1',
          agent_response: 'Test',
          response_status: 'success',
          response_latency_ms: 100,
          scores: [],
        },
      ],
    };

    apiClient.apiClient.listEvaluations.mockResolvedValue({
      data: mockEvaluations,
    });

    apiClient.apiClient.getEvaluationResults.mockResolvedValue({
      data: mockResults,
    });

    // Mock URL and document methods
    const mockCreateObjectURL = vi.fn(() => 'blob:mock');
    const mockRevokeObjectURL = vi.fn();
    global.URL.createObjectURL = mockCreateObjectURL;
    global.URL.revokeObjectURL = mockRevokeObjectURL;

    const { container } = render(<ResultsViewer />);

    await waitFor(() => {
      fireEvent.click(screen.getByText('123abc...'));
    });

    await waitFor(() => {
      fireEvent.click(screen.getByText('Export JSON'));
    });

    await waitFor(() => {
      expect(mockCreateObjectURL).toHaveBeenCalled();
      expect(mockRevokeObjectURL).toHaveBeenCalled();
    });
  });
});
