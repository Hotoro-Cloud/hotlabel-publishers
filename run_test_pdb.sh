#!/bin/bash

# This script runs a specific test with the Python debugger (pdb)

# Check if test ID is provided
if [ -z "$1" ]; then
    echo "Error: No test ID provided."
    echo "Usage: $0 <test_id>"
    echo "Example: $0 tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data"
    exit 1
fi

TEST_ID=$1

# Run the specified test with pdb
echo "Running test with ID: $TEST_ID with pdb debugger..."
pytest "$TEST_ID" -v --pdb

echo ""
echo "PDB Debugger Commands:"
echo "c: continue execution"
echo "n: next line"
echo "s: step into function call"
echo "l: list source code"
echo "p <expression>: print expression"
echo "h: help"
echo "q: quit debugger"
