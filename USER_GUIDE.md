# Agent Evaluation Service - User Guide

## Welcome to Agent Evaluation Service! 👋

This guide helps you get started with evaluating AI agent responses systematically.

## Getting Started

### 1. **Create Test Cases** (Tab: "Test Cases")

Define what you want to test your agent on.

#### How to Create a Test Case
1. Click **Test Cases** tab
2. Click **"Add New Test Case"** button
3. Fill in the form:
   - **Input**: What you're asking the agent (e.g., "What is 2+2?")
   - **Expected Output**: What the correct answer should be (e.g., "4")
   - **Description**: Optional context (e.g., "Basic math test")
   - **Tags**: Optional labels for organization (e.g., "math", "basic")
4. Click **Create Test Case**

#### View Your Test Cases
- All created test cases appear in a table below the form
- Each test case shows:
  - Input and expected output
  - Description and tags
  - Created/modified timestamps
- **Actions**:
  - 👁 **View**: See test case details
  - 🗑 **Delete**: Remove test case

#### Tips
- Use consistent formatting for inputs/outputs
- Add descriptive tags for easy filtering
- Create test cases for different scenarios (edge cases, normal cases, error cases)

### 2. **Run Evaluations** (Tab: "Run Evaluation")

Execute your test cases against your AI agent.

#### How to Run an Evaluation
1. Click **Run Evaluation** tab
2. Configure the evaluation:
   - **Agent Endpoint URL**: Where your agent API runs (e.g., "http://localhost:9000/agent")
   - **Select Test Cases**: Check the test cases you want to evaluate
   - **Select Graders**: Choose how to score responses (currently "String Match" MVP)
3. Click **Start Evaluation**
4. See status: **Pending** → **Running** → **Completed**

#### String Match Grader Options
The String Match grader compares expected output to agent response:
- **Case Insensitive**: "Hello" matches "hello"
- **Whitespace Normalization** (optional): Ignores extra spaces

#### What Happens During Evaluation
1. For each test case, the agent is called with the input
2. The agent's response is captured
3. The grader evaluates if the response matches expected output
4. Results are collected in real-time

#### Timeouts
- Agent response: 30 seconds maximum
- Grader evaluation: 5 seconds maximum
- If exceeded, marked as "timeout"

### 3. **View Results** (Tab: "View Status")

Analyze and export evaluation results.

#### Results Dashboard

**Left Sidebar: Recent Evaluations**
- Shows list of recent evaluation runs
- Click on a run to view its detailed results
- Status indicator shows run status:
  - **P**: Pending
  - **R**: Running
  - **C**: Completed
  - **F**: Failed

**Main Area: Results Details**

When you select an evaluation run:

1. **Summary Statistics** (Top cards)
   - Total Results: How many test cases were evaluated
   - Successful: How many passed
   - Failed: How many failed
   - Timeout: How many timed out
   - Avg Latency: Average response time in milliseconds

2. **Filter by Status** (Dropdown)
   - View all results
   - View only successful responses
   - View only errors
   - View only timeouts

3. **Results Table**
   - **Test Case**: ID of the test case
   - **Agent Response**: What the agent returned
   - **Status**: success, error, or timeout
   - **Latency**: How long the response took
   - **Scores**: How many graders passed (e.g., "1/1 ✓")

#### Interpreting Results

| Status | Meaning | Action |
|--------|---------|--------|
| ✓ Success | Agent responded and grader passed | Review output if needed |
| ✗ Error | Agent failed or returned error | Check agent logs |
| ⏱ Timeout | Response took too long | Increase timeout or optimize agent |

#### Export Results

**Export as JSON**
- Contains complete evaluation metadata
- Includes all grader details
- Best for: Data analysis, archival, integration

**Export as CSV**
- Spreadsheet format (Excel, Sheets)
- Easier for: Sharing with team, manual analysis

### Key Features

✅ **Test Case Management**
- Create, edit, view, delete test cases
- Tag-based organization
- Timestamp tracking

✅ **Async Evaluation**
- Run multiple test cases simultaneously
- Real-time progress tracking
- Background processing

✅ **Flexible Grading**
- Multiple graders per evaluation
- Per-result error isolation (one failed grader doesn't fail all)
- Extensible grader system

✅ **Results Analysis**
- Status-based filtering
- Summary statistics
- Per-result detail view
- JSON/CSV export

✅ **Responsive Design**
- Works on desktop, tablet, mobile
- Intuitive navigation
- Real-time updates

## Common Workflows

### Workflow 1: Test Your Agent's Math Skills
1. Create test cases with math problems
   - Input: "What is 15 * 3?"
   - Expected: "45"
2. Configure agent endpoint
3. Run evaluation on all math test cases
4. Review successful vs. failed responses
5. Export results for analysis

### Workflow 2: Test Consistency
1. Create same question as multiple test cases
   - Different phrasings of same question
2. Run evaluation
3. Check if agent responds consistently
4. Identify response variability

### Workflow 3: Performance Benchmarking
1. Create test cases across difficulty levels
2. Run evaluation with timing enabled
3. Review latency column
4. Identify performance bottlenecks

### Workflow 4: Error Analysis
1. Run evaluation on all test cases
2. Filter by "Error" status
3. Review error messages
4. Fix agent issues
5. Re-run evaluation

## Tips & Best Practices

### Test Case Design
- ✅ Use clear, unambiguous inputs
- ✅ Define precise expected outputs
- ✅ Create edge cases (empty inputs, large inputs, special characters)
- ✅ Test error scenarios
- ✅ Use descriptive tags
- ❌ Don't mix multiple questions in one test case

### Evaluation Setup
- ✅ Start with small test case sets (5-10) for quick feedback
- ✅ Verify agent endpoint is running before evaluation
- ✅ Use mock agent for testing (localhost:9000)
- ✅ Keep agent response time under 10s for good UX
- ❌ Don't use unreachable endpoints

### Result Analysis
- ✅ Check average latency for performance issues
- ✅ Review failed cases first
- ✅ Look for patterns in failures
- ✅ Use CSV export for statistical analysis
- ✅ Tag test cases to categorize results
- ❌ Don't assume correlation is causation

## Troubleshooting

### "Agent endpoint unreachable"
- Check agent is running
- Verify URL is correct
- Check firewall/network settings
- Test with curl: `curl http://endpoint/agent`

### "Timeout - Agent took too long"
- Increase timeout settings in config
- Optimize agent performance
- Split test cases into smaller batches
- Check for agent resource constraints

### "Export failed"
- Ensure evaluation is completed
- Try different format (JSON then CSV or vice versa)
- Check browser console for errors
- Refresh page and try again

### "No results showing"
- Wait for evaluation to complete
- Click on evaluation run to select it
- Check filter settings
- Try refreshing page

## API Integration (for Developers)

If integrating with your own systems:

```javascript
// Get evaluations
GET /api/evaluations

// Get specific results
GET /api/evaluations/{id}/results

// Export as JSON (client-side)
// Use browser download feature

// Create test case
POST /api/test-cases
Body: {
  "input": "...",
  "expected_output": "...",
  "description": "...",
  "tags": [...]
}
```

See [API Documentation](./README.md) for full endpoint reference.

## Getting Help

### Common Questions

**Q: Can I edit a test case after creating it?**
A: Click the edit icon next to a test case to modify it.

**Q: Can I re-run the same evaluation?**
A: Create a new evaluation with the same test cases.

**Q: How long are results stored?**
A: Currently in-memory (lost on restart). Database support coming soon.

**Q: Can I use custom graders?**
A: Yes! See [Developer Guide](./DEVELOPER_GUIDE.md) for custom grader implementation.

**Q: What if my agent needs specific headers/authentication?**
A: Modify the agent configuration or contact system administrator.

## Feedback & Support

Found a bug? Have a feature request?
- Check [GitHub Issues](https://github.com/)
- Or contact the development team

## Next Steps

1. ✅ Create 5-10 test cases
2. ✅ Set up your agent endpoint
3. ✅ Run your first evaluation
4. ✅ Review results
5. ✅ Export and analyze
6. ✅ Iterate and improve

Happy evaluating! 🚀
