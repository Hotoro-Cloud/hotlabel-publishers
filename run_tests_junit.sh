#!/bin/bash

# This script runs tests and generates a JUnit XML report

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating JUnit XML report..."
pytest --junitxml=test_reports/junit.xml --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "JUnit XML report generated at test_reports/junit.xml"
else
    echo "Some tests failed. Please check the output above for details."
    echo "JUnit XML report generated at test_reports/junit.xml"
fi
