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
