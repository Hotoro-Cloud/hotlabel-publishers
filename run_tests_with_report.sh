#!/bin/bash

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

# Run tests with coverage and generate reports
echo "Running tests with coverage and generating reports..."
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml:test_reports/coverage.xml --junitxml=test_reports/junit.xml

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "Coverage report generated in htmlcov/ directory"
    echo "Open htmlcov/index.html in your browser to view the report"
    echo "JUnit XML report generated at test_reports/junit.xml"
    echo "Coverage XML report generated at test_reports/coverage.xml"
    
    # Generate coverage badge
    echo "Generating coverage badge..."
    ./generate_coverage_badge.py
else
    echo "Some tests failed. Please check the output above for details."
fi
