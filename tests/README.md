# HotLabel Publishers Tests

This directory contains tests for the HotLabel Publishers API.

## Test Structure

The tests are organized into the following directories:

- `unit/`: Unit tests for individual components
  - `test_schemas.py`: Tests for Pydantic schemas
  - `test_crud.py`: Tests for CRUD operations
  - `test_auth.py`: Tests for authentication
  - `test_main.py`: Tests for main application endpoints
  - `test_config.py`: Tests for configuration
  - `test_database.py`: Tests for database operations
  - `test_models.py`: Tests for database models

- `integration/`: Integration tests for multiple components
  - `test_api_routes.py`: Tests for API routes
  - `test_db.py`: Tests for database integration

- `e2e/`: End-to-end tests for complete workflows
  - `test_publisher_lifecycle.py`: Tests for the complete publisher lifecycle

## Running Tests

### Prerequisites

Make sure you have installed all the required dependencies:

```bash
# Install all dependencies manually
pip install -r requirements.txt

# Or use the provided script
./install_test_dependencies.sh
```

### Cleaning Test Artifacts

To clean up test artifacts (coverage files, cache, reports, etc.):

```bash
./clean_test_artifacts.sh
```

This will remove:
- Coverage files (.coverage, htmlcov/, coverage.xml)
- Pytest cache (.pytest_cache/)
- Test reports (test_reports/)
- Python cache files (__pycache__ directories, .pyc files)

### Running All Tests

To run all tests:

```bash
# Using pytest directly
pytest

# Using the provided script
./run_tests.sh
```

### Running All Test Scripts

To run all test scripts in sequence:

```bash
./run_all_test_scripts.sh
```

This will run all the test scripts in sequence, including:
1. Basic tests
2. Unit tests
3. Integration tests
4. End-to-end tests
5. Tests with coverage report
6. Tests with summary
7. Tests with JUnit XML report
8. Tests with HTML report
9. Tests with JSON report
10. Tests with CSV report
11. Tests with Markdown report
12. Tests with interactive single HTML report
13. Tests with duration report
14. Tests in parallel
15. Tests in random order
16. Tests stopping on first failure
17. Tests with all report formats

### Running Tests in Parallel

To run tests in parallel (faster execution on multi-core systems):

```bash
# Using pytest directly with 4 processes
pytest -n 4 --cov=app

# Using the provided script (automatically uses all CPU cores)
./run_tests_parallel.sh

# Using the provided script with a specific number of processes
./run_tests_parallel.sh 2
```

Note: Parallel test execution requires pytest-xdist, which is included in the requirements.txt file.

### Running Tests in Random Order

To run tests in random order (helps identify test interdependencies):

```bash
# Using pytest directly
pytest --random-order --cov=app

# Using the provided script
./run_tests_random_order.sh
```

To reproduce a specific random order, use the seed from a previous run:

```bash
pytest --random-order-seed=1234 --cov=app
```

Note: Random order execution requires pytest-random-order, which is included in the requirements.txt file.

### Running Specific Test Categories

To run unit tests only:

```bash
# Using pytest directly
pytest tests/unit/

# Using the provided script
./run_unit_tests.sh
```

To run integration tests only:

```bash
# Using pytest directly
pytest tests/integration/

# Using the provided script
./run_integration_tests.sh
```

To run end-to-end tests only:

```bash
# Using pytest directly
pytest tests/e2e/

# Using the provided script
./run_e2e_tests.sh
```

### Running Tests with Coverage

To run tests with coverage report:

```bash
# Basic coverage report
pytest --cov=app --cov-report=term-missing

# Comprehensive coverage report with HTML and XML output
./run_tests_with_report.sh

# Generate coverage reports with test summary
./run_tests_with_summary.sh

# Generate coverage reports for CI/CD systems
./run_tests_ci.sh

# Generate all report formats at once
./run_tests_all_reports.sh
```

The `run_tests_all_reports.sh` script generates all report formats in a single run:
- HTML coverage report (htmlcov/index.html)
- XML coverage report (test_reports/coverage.xml)
- JUnit XML report (test_reports/junit.xml)
- HTML report (test_reports/report.html)
- JSON report (test_reports/report.json)
- CSV report (test_reports/report.csv)
- Markdown report (test_reports/report.md)
- Single HTML report (test_reports/report_single.html)

### Running Tests with Duration Report

To run tests and report the slowest tests:

```bash
# Using pytest directly (report 10 slowest tests)
pytest --durations=10 --cov=app

# Using the provided script (report 10 slowest tests by default)
./run_tests_with_durations.sh

# Using the provided script with a custom number of tests to report
./run_tests_with_durations.sh 5
```

This is useful for identifying slow tests that might need optimization.

### Running Tests with JUnit XML Report

To run tests and generate a JUnit XML report:

```bash
# Using pytest directly
pytest --junitxml=test_reports/junit.xml --cov=app

# Using the provided script
./run_tests_junit.sh
```

This is useful for integrating with CI/CD systems and test reporting tools.

### Running Tests with HTML Report

To run tests and generate an HTML report:

```bash
# Using pytest directly
pytest --html=test_reports/report.html --self-contained-html --cov=app

# Using the provided script
./run_tests_html_report.sh
```

This generates a self-contained HTML report with test results that can be viewed in a browser.

### Running Tests with Interactive Single HTML Report

To run tests and generate an interactive single HTML report:

```bash
# Using the provided script
./run_tests_single_html.sh
```

This script runs the tests, generates a JSON report, and then converts it to a single HTML file with:
- Interactive filtering (all tests, failed tests, passed tests, skipped tests)
- Test summary with percentages
- Coverage information
- Failed tests with error messages
- Complete test list with color-coded outcomes

### Running Tests with JSON Report

To run tests and generate a JSON report:

```bash
# Using pytest directly
pytest --json-report --json-report-file=test_reports/report.json --cov=app

# Using the provided script
./run_tests_json_report.sh
```

This generates a JSON report with test results that can be used for programmatic analysis or integration with other tools.

### Running Tests with CSV Report

To run tests and generate a CSV report:

```bash
# Using the provided script
./run_tests_csv_report.sh
```

This script runs the tests, generates a JSON report, and then converts it to a CSV format for easy import into spreadsheet applications or data analysis tools.

### Running Tests with Markdown Report

To run tests and generate a Markdown report:

```bash
# Using the provided script
./run_tests_markdown_report.sh
```

This script runs the tests, generates a JSON report, and then converts it to a Markdown format with:
- Test summary (total, passed, failed, skipped)
- Coverage information
- Failed tests with error messages
- Slowest tests
- Complete test list

### Running Tests with Verbose Output

To run tests with verbose output:

```bash
# Using pytest directly
pytest -v --cov=app

# Using the provided script
./run_tests_verbose.sh
```

### Running Tests and Stopping on First Failure

To run tests and stop on the first failure:

```bash
# Using pytest directly
pytest -xvs --cov=app

# Using the provided script
./run_tests_stop_on_first_fail.sh
```

This is useful when you have many tests and want to fix failures one at a time.

### Running Tests by Marker

To run tests with a specific marker:

```bash
# Using pytest directly
pytest -m "unit" --cov=app

# Using the provided script
./run_tests_by_marker.sh unit
```

Available markers:
- `unit`: Unit tests
- `integration`: Integration tests
- `e2e`: End-to-end tests
- `schemas`: Tests for Pydantic schemas
- `crud`: Tests for CRUD operations
- `auth`: Tests for authentication
- `api`: Tests for API routes
- `db`: Tests for database operations

### Running Tests by Keyword

To run tests that match a specific keyword:

```bash
# Using pytest directly
pytest -k "publisher" --cov=app

# Using the provided script
./run_tests_by_keyword.sh publisher
```

### Running Tests by Path Pattern

To run tests that match a specific path pattern:

```bash
# Using pytest directly
pytest tests/unit/test_schemas.py --cov=app

# Using the provided script
./run_tests_by_path.sh tests/unit/test_schemas.py
```

### Running Failed Tests

To run only the tests that failed in the previous run:

```bash
# Using pytest directly
pytest --lf --cov=app

# Using the provided script
./run_failed_tests.sh
```

### Running Tests in Docker

To run tests in a clean Docker environment:

```bash
./run_tests_in_docker.sh
```

### Running Specific Test Files

To run a specific test file:

```bash
# Using pytest directly
pytest tests/unit/test_schemas.py

# Using the provided script
./run_tests_by_path.sh tests/unit/test_schemas.py
```

### Running Specific Test Functions

To run a specific test function:

```bash
# Using pytest directly
pytest tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data

# Using the provided script
./run_test_by_id.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data
```

### Debugging Tests

To run a specific test in debug mode with local variables displayed:

```bash
# Using pytest directly
pytest tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data -v --showlocals

# Using the provided script
./run_test_debug.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data
```

To run a specific test with the Python debugger (pdb):

```bash
# Using pytest directly
pytest tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data -v --pdb

# Using the provided script
./run_test_pdb.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data
```

Common pdb commands:
- `c`: continue execution
- `n`: next line
- `s`: step into function call
- `l`: list source code
- `p <expression>`: print expression
- `h`: help
- `q`: quit debugger

### Testing for Flaky Tests

To run a specific test repeatedly until it fails (useful for finding flaky tests):

```bash
# Using the provided script
./run_test_until_failure.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data

# Using the provided script with a custom number of iterations
./run_test_until_failure.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data 500
```

This is useful for identifying tests that fail intermittently due to race conditions, timing issues, or other non-deterministic factors.

### Listing All Available Tests

To list all available tests:

```bash
# Using pytest directly
pytest --collect-only -v

# Using the provided script
./list_tests.sh
```

## Test Fixtures

The test fixtures are defined in `conftest.py`. The main fixtures are:

- `engine`: SQLAlchemy engine for testing with in-memory SQLite database
- `db_session`: SQLAlchemy session for database operations
- `client`: FastAPI TestClient for API testing
- `sample_publisher_data`: Sample data for creating a publisher
- `sample_publisher_in_db`: A publisher instance already saved in the database

## Test Configuration

The test configuration is defined in `pytest.ini`. It includes:

- Test paths and patterns
- Test verbosity
- Coverage configuration
- Test markers

## Continuous Integration

Tests are automatically run on GitHub Actions when code is pushed or a pull request is created. The workflow is defined in `.github/workflows/tests.yml`.

## Coverage Badge

A coverage badge is generated after running tests with the `generate_coverage_badge.py` script. This badge can be included in the README to show the current test coverage.

## Adding New Tests

When adding new tests, follow these guidelines:

1. Place unit tests in the `unit/` directory
2. Place integration tests in the `integration/` directory
3. Place end-to-end tests in the `e2e/` directory
4. Use appropriate fixtures from `conftest.py`
5. Follow the naming convention: `test_*.py` for files, `Test*` for classes, and `test_*` for functions
6. Add appropriate markers to categorize tests
7. Ensure tests are independent and can run in any order
8. Aim for high code coverage, especially for critical components
