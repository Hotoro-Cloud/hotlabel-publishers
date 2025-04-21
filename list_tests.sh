#!/bin/bash

# This script lists all available tests

echo "Listing all available tests..."
pytest --collect-only -v

echo ""
echo "To run a specific test, use:"
echo "./run_test_by_id.sh <test_id>"
echo ""
echo "Example:"
echo "./run_test_by_id.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data"
