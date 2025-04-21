#!/bin/bash

# Run tests with coverage and generate HTML report
echo "Running tests with coverage..."
pytest --cov=app --cov-report=term-missing --cov-report=html

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "Coverage report generated in htmlcov/ directory"
    echo "Open htmlcov/index.html in your browser to view the report"
else
    echo "Some tests failed. Please check the output above for details."
fi
