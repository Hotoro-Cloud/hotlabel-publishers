#!/bin/bash

# This script runs tests and generates a single HTML report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating single HTML report..."

# Run tests and generate a JSON report first
pytest --json-report --json-report-file=test_reports/report.json --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi

# Convert JSON report to a single HTML file
echo "Converting JSON report to HTML..."
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
    message = test_data.get('message', '').replace('\n', '<br>')
    results.append((test_id, outcome, duration, message))

# Sort by outcome (failed first) and then by duration (slowest first)
results.sort(key=lambda x: (0 if x[1] == 'failed' else 1, -x[2]))

# Generate HTML report
with open('test_reports/report_single.html', 'w') as f:
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang=\"en\">\n')
    f.write('<head>\n')
    f.write('    <meta charset=\"UTF-8\">\n')
    f.write('    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n')
    f.write('    <title>Test Report</title>\n')
    f.write('    <style>\n')
    f.write('        body { font-family: Arial, sans-serif; margin: 20px; }\n')
    f.write('        h1, h2 { color: #333; }\n')
    f.write('        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }\n')
    f.write('        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n')
    f.write('        th { background-color: #f2f2f2; }\n')
    f.write('        tr:nth-child(even) { background-color: #f9f9f9; }\n')
    f.write('        .passed { color: green; }\n')
    f.write('        .failed { color: red; }\n')
    f.write('        .skipped { color: orange; }\n')
    f.write('        .unknown { color: gray; }\n')
    f.write('        .summary { display: flex; justify-content: space-between; flex-wrap: wrap; }\n')
    f.write('        .summary-box { border: 1px solid #ddd; padding: 10px; margin: 10px; flex: 1; min-width: 200px; }\n')
    f.write('        .filter-buttons { margin-bottom: 20px; }\n')
    f.write('        .filter-buttons button { margin-right: 10px; padding: 5px 10px; cursor: pointer; }\n')
    f.write('    </style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    
    # Header
    f.write(f'    <h1>Test Report</h1>\n')
    f.write(f'    <p>Generated on: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}</p>\n')
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r[1] == 'passed')
    failed = sum(1 for r in results if r[1] == 'failed')
    skipped = sum(1 for r in results if r[1] == 'skipped')
    
    f.write('    <h2>Summary</h2>\n')
    f.write('    <div class=\"summary\">\n')
    f.write('        <div class=\"summary-box\">\n')
    f.write(f'            <h3>Tests</h3>\n')
    f.write(f'            <p>Total: {total}</p>\n')
    f.write(f'            <p class=\"passed\">Passed: {passed} ({passed/total*100:.1f}%)</p>\n')
    f.write(f'            <p class=\"failed\">Failed: {failed} ({failed/total*100:.1f}%)</p>\n')
    f.write(f'            <p class=\"skipped\">Skipped: {skipped} ({skipped/total*100:.1f}%)</p>\n')
    f.write('        </div>\n')
    
    # Coverage
    if 'summary' in data and 'coverage' in data['summary']:
        cov = data['summary']['coverage']
        f.write('        <div class=\"summary-box\">\n')
        f.write(f'            <h3>Coverage</h3>\n')
        f.write(f'            <p>Coverage: {cov.get(\"coverage_percent\", 0):.1f}%</p>\n')
        f.write(f'            <p>Covered lines: {cov.get(\"covered_lines\", 0)}</p>\n')
        f.write(f'            <p>Total lines: {cov.get(\"total_lines\", 0)}</p>\n')
        f.write('        </div>\n')
    
    f.write('    </div>\n')
    
    # Filter buttons
    f.write('    <div class=\"filter-buttons\">\n')
    f.write('        <button onclick=\"showAll()\">All Tests</button>\n')
    f.write('        <button onclick=\"showFailed()\">Failed Tests</button>\n')
    f.write('        <button onclick=\"showPassed()\">Passed Tests</button>\n')
    f.write('        <button onclick=\"showSkipped()\">Skipped Tests</button>\n')
    f.write('    </div>\n')
    
    # Failed tests
    if failed > 0:
        f.write('    <h2>Failed Tests</h2>\n')
        f.write('    <table id=\"failed-tests\">\n')
        f.write('        <tr><th>Test ID</th><th>Duration (s)</th><th>Message</th></tr>\n')
        for test_id, outcome, duration, message in results:
            if outcome == 'failed':
                f.write(f'        <tr><td>{test_id}</td><td>{duration:.3f}</td><td>{message}</td></tr>\n')
        f.write('    </table>\n')
    
    # All tests
    f.write('    <h2>All Tests</h2>\n')
    f.write('    <table id=\"all-tests\">\n')
    f.write('        <tr><th>Test ID</th><th>Outcome</th><th>Duration (s)</th></tr>\n')
    for test_id, outcome, duration, _ in results:
        f.write(f'        <tr class=\"{outcome}\"><td>{test_id}</td><td class=\"{outcome}\">{outcome}</td><td>{duration:.3f}</td></tr>\n')
    f.write('    </table>\n')
    
    # JavaScript for filtering
    f.write('    <script>\n')
    f.write('        function showAll() {\n')
    f.write('            const rows = document.querySelectorAll(\"#all-tests tr\");\n')
    f.write('            rows.forEach(row => {\n')
    f.write('                if (row.querySelector(\"th\")) return; // Skip header row\n')
    f.write('                row.style.display = \"\";\n')
    f.write('            });\n')
    f.write('        }\n')
    f.write('        \n')
    f.write('        function showFailed() {\n')
    f.write('            const rows = document.querySelectorAll(\"#all-tests tr\");\n')
    f.write('            rows.forEach(row => {\n')
    f.write('                if (row.querySelector(\"th\")) return; // Skip header row\n')
    f.write('                if (row.classList.contains(\"failed\")) {\n')
    f.write('                    row.style.display = \"\";\n')
    f.write('                } else {\n')
    f.write('                    row.style.display = \"none\";\n')
    f.write('                }\n')
    f.write('            });\n')
    f.write('        }\n')
    f.write('        \n')
    f.write('        function showPassed() {\n')
    f.write('            const rows = document.querySelectorAll(\"#all-tests tr\");\n')
    f.write('            rows.forEach(row => {\n')
    f.write('                if (row.querySelector(\"th\")) return; // Skip header row\n')
    f.write('                if (row.classList.contains(\"passed\")) {\n')
    f.write('                    row.style.display = \"\";\n')
    f.write('                } else {\n')
    f.write('                    row.style.display = \"none\";\n')
    f.write('                }\n')
    f.write('            });\n')
    f.write('        }\n')
    f.write('        \n')
    f.write('        function showSkipped() {\n')
    f.write('            const rows = document.querySelectorAll(\"#all-tests tr\");\n')
    f.write('            rows.forEach(row => {\n')
    f.write('                if (row.querySelector(\"th\")) return; // Skip header row\n')
    f.write('                if (row.classList.contains(\"skipped\")) {\n')
    f.write('                    row.style.display = \"\";\n')
    f.write('                } else {\n')
    f.write('                    row.style.display = \"none\";\n')
    f.write('                }\n')
    f.write('            });\n')
    f.write('        }\n')
    f.write('    </script>\n')
    
    f.write('</body>\n')
    f.write('</html>\n')

print('Single HTML report generated with interactive filtering')
"

echo "Single HTML report generated at test_reports/report_single.html"
