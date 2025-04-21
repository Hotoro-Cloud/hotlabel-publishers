#!/bin/bash

# This script runs tests and generates a Markdown report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating Markdown report..."

# Run tests and generate a JSON report first
pytest --json-report --json-report-file=test_reports/report.json --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi

# Convert JSON report to Markdown
echo "Converting JSON report to Markdown..."
python -c "
import json
import os
from datetime import datetime

# Load JSON report
with open('test_reports/report.json', 'r') as f:
    data = json.load(f)

# Extract test results
results = []
for test_id, test_data in data.get('tests', {}).items():
    outcome = test_data.get('outcome', 'unknown')
    duration = test_data.get('duration', 0)
    message = test_data.get('message', '').replace('\n', ' ')
    results.append((test_id, outcome, duration, message))

# Sort by outcome (failed first) and then by duration (slowest first)
results.sort(key=lambda x: (0 if x[1] == 'failed' else 1, -x[2]))

# Generate Markdown report
with open('test_reports/report.md', 'w') as f:
    f.write('# Test Report\n\n')
    f.write(f'Generated on: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}\n\n')
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r[1] == 'passed')
    failed = sum(1 for r in results if r[1] == 'failed')
    skipped = sum(1 for r in results if r[1] == 'skipped')
    
    f.write('## Summary\n\n')
    f.write(f'- Total tests: {total}\n')
    f.write(f'- Passed: {passed} ({passed/total*100:.1f}%)\n')
    f.write(f'- Failed: {failed} ({failed/total*100:.1f}%)\n')
    f.write(f'- Skipped: {skipped} ({skipped/total*100:.1f}%)\n\n')
    
    # Coverage
    if 'summary' in data and 'coverage' in data['summary']:
        cov = data['summary']['coverage']
        f.write('## Coverage\n\n')
        f.write(f'- Coverage: {cov.get(\"coverage_percent\", 0):.1f}%\n')
        f.write(f'- Covered lines: {cov.get(\"covered_lines\", 0)}\n')
        f.write(f'- Total lines: {cov.get(\"total_lines\", 0)}\n\n')
    
    # Failed tests
    if failed > 0:
        f.write('## Failed Tests\n\n')
        f.write('| Test ID | Duration (s) | Message |\n')
        f.write('|---------|--------------|--------|\n')
        for test_id, outcome, duration, message in results:
            if outcome == 'failed':
                f.write(f'| {test_id} | {duration:.3f} | {message} |\n')
        f.write('\n')
    
    # Slow tests
    f.write('## Slowest Tests\n\n')
    f.write('| Test ID | Outcome | Duration (s) |\n')
    f.write('|---------|---------|---------------|\n')
    for test_id, outcome, duration, _ in sorted(results, key=lambda x: -x[2])[:10]:
        f.write(f'| {test_id} | {outcome} | {duration:.3f} |\n')
    f.write('\n')
    
    # All tests
    f.write('## All Tests\n\n')
    f.write('| Test ID | Outcome | Duration (s) |\n')
    f.write('|---------|---------|---------------|\n')
    for test_id, outcome, duration, _ in results:
        f.write(f'| {test_id} | {outcome} | {duration:.3f} |\n')

print(f'Markdown report generated with {len(results)} test results')
"

echo "Markdown report generated at test_reports/report.md"
