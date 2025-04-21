#!/bin/bash

# This script runs tests and generates a CSV report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating CSV report..."

# Run tests and generate a JSON report first
pytest --json-report --json-report-file=test_reports/report.json --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi

# Convert JSON report to CSV
echo "Converting JSON report to CSV..."
echo "test_id,outcome,duration,message" > test_reports/report.csv
python -c "
import json
import csv
import os

# Load JSON report
with open('test_reports/report.json', 'r') as f:
    data = json.load(f)

# Extract test results
results = []
for test_id, test_data in data.get('tests', {}).items():
    outcome = test_data.get('outcome', 'unknown')
    duration = test_data.get('duration', 0)
    message = test_data.get('message', '').replace('\n', ' ').replace(',', ';')
    results.append([test_id, outcome, duration, message])

# Write to CSV
with open('test_reports/report.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerows(results)

print(f'CSV report generated with {len(results)} test results')
"

echo "CSV report generated at test_reports/report.csv"
