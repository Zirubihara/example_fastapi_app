# FastAPI Example Application

A modern FastAPI application demonstrating best practices in project structure, testing, and deployment.

## Features

- RESTful API endpoints
- PostgreSQL database integration
- Alembic migrations
- Comprehensive testing suite
- Docker support
- CI/CD pipeline
- API documentation

## Requirements

- Python 3.9+
- PostgreSQL
- Docker (optional)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/example_fastapi_app.git
   cd example_fastapi_app
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

3. Install dependencies:

   ```bash
   make install
   ```

4. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

5. Run database migrations:

   ```bash
   make migrate
   ```

## Development

Start the development server:

```bash
make run
```

Run tests:

```bash
make test
```

Format code:

```bash
make format
```

Run linting:

```bash
make lint
```

## Docker

Start with Docker Compose:

```bash
make docker-up
```

Stop containers:

```bash
make docker-down
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
