import { useState } from 'react'
import TestCaseManager from './TestCaseManager'
import EvaluationRunner from '../components/EvaluationRunner'
import ResultsViewer from '../components/ResultsViewer'

export default function App() {
  const [activeTab, setActiveTab] = useState('test-cases')

  return (
    <div className="app">
      <header className="app-header">
        <h1>Agent Evaluation Service</h1>
        <p>Define test cases, run evaluations, and score responses</p>
      </header>

      <nav className="app-nav">
        <button 
          className={`nav-btn ${activeTab === 'test-cases' ? 'active' : ''}`}
          onClick={() => setActiveTab('test-cases')}
        >
          Test Cases
        </button>
        <button 
          className={`nav-btn ${activeTab === 'runner' ? 'active' : ''}`}
          onClick={() => setActiveTab('runner')}
        >
          Run Evaluation
        </button>
        <button 
          className={`nav-btn ${activeTab === 'results' ? 'active' : ''}`}
          onClick={() => setActiveTab('results')}
        >
          View Status
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'test-cases' && <TestCaseManager />}
        {activeTab === 'runner' && <EvaluationRunner />}
        {activeTab === 'results' && <ResultsViewer />}
      </main>
    </div>
  )
}
