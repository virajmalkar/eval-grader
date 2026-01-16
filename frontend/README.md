# Agent Evaluation Service - Frontend

React + Vite frontend for the Agent Evaluation Service.

## Setup

### Prerequisites
- Node.js 16+
- npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file (if needed):
```bash
cp .env.example .env.local
```

## Development

```bash
# Start dev server (port 5173)
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Type check (if using TypeScript)
npm run type-check
```

## Project Structure

- `src/pages/` - Page components (App.jsx, TestCaseManager.jsx)
- `src/components/` - Reusable components
  - `TestCaseForm.jsx` - Create/edit test cases
  - `TestCaseList.jsx` - Display test cases
  - `EvaluationRunner.jsx` - Run evaluations
  - `ResultsViewer.jsx` - View and export results
  - `GraderSelector.jsx` - Select graders
- `src/services/` - API client
- `src/styles/` - CSS styling

## Features

### Test Case Management
- Create test cases with input, expected output, description, and tags
- List all test cases with filtering
- Edit and delete test cases

### Evaluation Execution
- Select test cases to evaluate
- Choose agent endpoint
- Select graders to apply
- Run evaluation asynchronously

### Results Viewer
- View evaluation results in real-time
- Filter results by status (success, error, timeout)
- Summary statistics (total, successful, failed, average latency)
- Export results as JSON or CSV
- Per-result scoring details

## API Client

The `APIClient` class in `src/services/api.js` handles all backend communication:

```javascript
import { apiClient } from './services/api';

// Test cases
await apiClient.createTestCase(data);
await apiClient.listTestCases(skip, limit);
await apiClient.getTestCase(id);
await apiClient.updateTestCase(id, data);
await apiClient.deleteTestCase(id);

// Evaluations
await apiClient.createEvaluation(data);
await apiClient.getEvaluationStatus(id);
await apiClient.listEvaluations(skip, limit);
await apiClient.getEvaluationResults(id);

// Graders
await apiClient.listGraders();
await apiClient.getGrader(id);
```

## Testing

Tests use Vitest and testing-library:

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

Test files are located in `tests/` directory with `.test.jsx` extension.

## Styling

The application uses CSS with CSS variables for theming:

- Primary color: #2563eb
- Success: #10b981
- Error: #ef4444
- Warning: #f59e0b

All components are responsive and work on mobile, tablet, and desktop devices.

## Deployment

```bash
# Build for production
npm run build

# The output is in the `dist/` directory
```

The built app can be served by any static file server. Ensure the `/api` routes are proxied to the backend (default: localhost:8000).
