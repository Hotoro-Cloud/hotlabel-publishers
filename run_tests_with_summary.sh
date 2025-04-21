#!/bin/bash

# This script runs tests and generates a summary

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

echo "Running tests and generating summary..."
pytest -v --cov=app --cov-report=term-missing --cov-report=html

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi

# Generate summary
echo ""
echo "Test Summary:"
echo "============="
echo "Total tests: $(pytest --collect-only -q | wc -l)"
echo "Unit tests: $(pytest --collect-only -q tests/unit/ 2>/dev/null | wc -l)"
echo "Integration tests: $(pytest --collect-only -q tests/integration/ 2>/dev/null | wc -l)"
echo "End-to-end tests: $(pytest --collect-only -q tests/e2e/ 2>/dev/null | wc -l)"
echo ""
echo "Coverage report generated in htmlcov/ directory"
echo "Open htmlcov/index.html in your browser to view the report"
