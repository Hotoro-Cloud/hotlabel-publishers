#!/bin/bash

# This script runs tests and generates a JSON report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating JSON report..."
pytest --json-report --json-report-file=test_reports/report.json --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "JSON report generated at test_reports/report.json"
else
    echo "Some tests failed. Please check the output above for details."
    echo "JSON report generated at test_reports/report.json"
fi
