#!/bin/bash

# This script runs tests with JUnit XML output for CI/CD systems

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

# Run tests with JUnit XML output
echo "Running tests with JUnit XML output..."
pytest --junitxml=test_reports/junit.xml --cov=app --cov-report=xml:test_reports/coverage.xml

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "JUnit XML report generated at test_reports/junit.xml"
    echo "Coverage XML report generated at test_reports/coverage.xml"
else
    echo "Some tests failed. Please check the output above for details."
    echo "JUnit XML report generated at test_reports/junit.xml"
    echo "Coverage XML report generated at test_reports/coverage.xml"
fi
