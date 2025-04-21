#!/bin/bash

# Run integration tests with coverage
echo "Running integration tests with coverage..."
pytest tests/integration/ --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All integration tests passed!"
else
    echo "Some integration tests failed. Please check the output above for details."
fi
