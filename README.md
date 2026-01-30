# GoRest API Test Framework

A robust API testing framework for GoRest API built with Python, pytest, and requests library.

## Framework Architecture

### Project Structure

```
gorest-api-test/
├── application/
│   ├── user_client.py          # User API client wrapper
│   └── payload/
│       └── user_payload.py     # Payload builders
├── core/
│   ├── api/
│   │   └── api_client.py       # Base HTTP client for API requests
│   └── utils/
│       └── http_logger.py      # HTTP request/response logging utilities
├── tests/
│   ├── conftest.py             # Global pytest fixtures
│   ├── test_users_collection.py # User collection tests
│   └── user/
│       ├── conftest.py         # User-specific fixtures
│       └── test_user_resource.py # Individual user resource tests
├── pyproject.toml              # Project dependencies
└── pytest.ini                  # Pytest configuration
```

### Architecture Layers

**1. Core Layer** (`core/`)
- **api_client.py**: Base HTTP client that handles all API communication (GET, POST, PUT, DELETE)
- **http_logger.py**: Logging utilities that sanitize sensitive headers and log requests/responses

**2. Application Layer** (`application/`)
- **user_client.py**: High-level client for user operations built on top of APIClient
- **payload/**: Payload builders using Faker to generate test data

**3. Test Layer** (`tests/`)
- **conftest.py**: Session-level fixtures for authentication, API client, and user client setup
- **test files**: Test cases organized by resource (users collection, individual user resources)

### Key Components

| Component | Purpose |
|-----------|---------|
| [`APIClient`](core/api/api_client.py) | Base HTTP client with request/response logging |
| [`UserClient`](application/user_client.py) | User API operations wrapper |
| [`user_create_payload`](application/payload/user_payload.py) | Generate test user data |
| [`http_logger`](core/utils/http_logger.py) | Sanitize and log HTTP traffic |

## Setup Instructions

### Prerequisites
- Python 3.14+
- UV package manager
- GoRest API token

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sksingh329/gorest-api-test.git
cd gorest-api-test
```

2. **Install dependencies**
```bash
uv sync
```

3. **Set API token**
```bash
export API_TOKEN="<<go_rest_api_token>>"
```

> Get your API token from [GoRest API](https://gorest.co.in/)

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run specific test file
```bash
uv run pytest tests/test_users_collection.py
```

### Run specific test
```bash
uv run pytest tests/user/test_user_resource.py::test_get_user
```

### Run with coverage
```bash
uv run pytest --cov=application --cov=core
```

### Run with verbose output
```bash
uv run pytest -v
```

## Test Structure

The framework includes test coverage for:
- **User Collection**: List and create users
- **User Resources**: Get, update, delete individual users
- **Error Handling**: Duplicate email validation

### Example Test
```python
def test_create_user(user_client):
    payload = user_create_payload(status="inactive")
    response = user_client.create_user(payload=payload)
    
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]
```

## Configuration

- **Base URL**: `https://gorest.co.in/public/v2`
- **Default Timeout**: 20 seconds
- **Log Level**: INFO (configured in [pytest.ini](pytest.ini))
- **Python Version**: 3.14+ (see [.python-version](.python-version))

## Dependencies

- **requests** ≥2.32.5: HTTP client
- **faker** ≥40.1.0: Test data generation
- **pytest** ≥9.0.2: Test framework

## License

MIT License - See [LICENSE](LICENSE) file for details