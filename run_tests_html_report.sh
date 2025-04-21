#!/bin/bash

# This script runs tests and generates an HTML report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating HTML report..."
pytest --html=test_reports/report.html --self-contained-html --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "HTML report generated at test_reports/report.html"
else
    echo "Some tests failed. Please check the output above for details."
    echo "HTML report generated at test_reports/report.html"
fi
