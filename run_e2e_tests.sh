#!/bin/bash

# Run end-to-end tests with coverage
echo "Running end-to-end tests with coverage..."
pytest tests/e2e/ --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All end-to-end tests passed!"
else
    echo "Some end-to-end tests failed. Please check the output above for details."
fi
