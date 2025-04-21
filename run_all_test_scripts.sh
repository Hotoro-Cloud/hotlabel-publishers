#!/bin/bash

# This script runs all the test scripts in sequence

echo "Running all test scripts in sequence..."

# Create a directory for test reports if it doesn't exist
mkdir -p test_reports

# Run all test scripts
echo "1. Running basic tests..."
./run_tests.sh

echo "2. Running unit tests..."
./run_unit_tests.sh

echo "3. Running integration tests..."
./run_integration_tests.sh

echo "4. Running end-to-end tests..."
./run_e2e_tests.sh

echo "5. Running tests with coverage report..."
./run_tests_with_report.sh

echo "6. Running tests with summary..."
./run_tests_with_summary.sh

echo "7. Running tests with JUnit XML report..."
./run_tests_junit.sh

echo "8. Running tests with HTML report..."
./run_tests_html_report.sh

echo "9. Running tests with JSON report..."
./run_tests_json_report.sh

echo "10. Running tests with CSV report..."
./run_tests_csv_report.sh

echo "11. Running tests with Markdown report..."
./run_tests_markdown_report.sh

echo "12. Running tests with interactive single HTML report..."
./run_tests_single_html.sh

echo "13. Running tests with duration report..."
./run_tests_with_durations.sh

echo "14. Running tests in parallel..."
./run_tests_parallel.sh

echo "15. Running tests in random order..."
./run_tests_random_order.sh

echo "16. Running tests and stopping on first failure..."
./run_tests_stop_on_first_fail.sh

echo "17. Running tests with all report formats..."
./run_tests_all_reports.sh

echo "All test scripts completed!"
