# HotLabel Publisher Management Service

This microservice handles publisher registration, configuration, and management for the HotLabel platform.

## Features

- Publisher registration and management
- Publisher configuration management
- Statistics and reporting
- Integration code generation
- Webhook management

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- PostgreSQL
- Redis

### Running the Service

```bash
# Using Docker
docker-compose up -d

# Without Docker
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

The project includes a comprehensive test suite with unit tests, integration tests, and end-to-end tests.

### Test Structure

- `tests/unit/`: Unit tests for individual components
  - `test_schemas.py`: Tests for Pydantic schemas
  - `test_crud.py`: Tests for CRUD operations
  - `test_auth.py`: Tests for authentication
  - `test_main.py`: Tests for main application endpoints
  - `test_config.py`: Tests for configuration
  - `test_database.py`: Tests for database operations
  - `test_models.py`: Tests for database models

- `tests/integration/`: Integration tests for multiple components
  - `test_api_routes.py`: Tests for API routes
  - `test_db.py`: Tests for database integration

- `tests/e2e/`: End-to-end tests for complete workflows
  - `test_publisher_lifecycle.py`: Tests for the complete publisher lifecycle

### Installing Test Dependencies

Before running the tests, make sure you have all the required dependencies installed:

```bash
# Install all dependencies
./install_test_dependencies.sh
```

### Cleaning Test Artifacts

To clean up test artifacts (coverage files, cache, reports, etc.):

```bash
./clean_test_artifacts.sh
```

### Running Tests

The project includes many scripts for running tests in different ways:

```bash
# Run all tests
./run_tests.sh

# Run all test scripts in sequence
./run_all_test_scripts.sh

# Run specific test categories
./run_unit_tests.sh
./run_integration_tests.sh
./run_e2e_tests.sh

# Run tests with different options
./run_tests_verbose.sh
./run_tests_with_report.sh
./run_tests_parallel.sh
./run_tests_random_order.sh
./run_tests_stop_on_first_fail.sh
./run_tests_with_durations.sh
./run_tests_junit.sh
./run_tests_html_report.sh

# Run tests by specific criteria
./run_tests_by_marker.sh unit
./run_tests_by_keyword.sh publisher
./run_tests_by_path.sh tests/unit/test_schemas.py
./run_test_by_id.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data

# Debug tests
./run_test_debug.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data
./run_test_pdb.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data

# Find flaky tests
./run_test_until_failure.sh tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data

# List all available tests
./list_tests.sh
```

### Test Coverage

The test suite aims for high code coverage:
- 90%+ coverage for core business logic
- 80%+ coverage for API routes
- 70%+ overall coverage

To view the coverage report:

```bash
# Generate HTML coverage report
./run_tests_with_report.sh

# Generate HTML coverage report with test summary
./run_tests_with_summary.sh

# Then open htmlcov/index.html in your browser
```

### Coverage Badge

A coverage badge is generated after running tests with the `generate_coverage_badge.py` script:

```bash
./generate_coverage_badge.py
```

### Continuous Integration

Tests are automatically run on GitHub Actions when code is pushed or a pull request is created. The workflow is defined in `.github/workflows/tests.yml`.

For more details about testing, see [tests/README.md](tests/README.md).
