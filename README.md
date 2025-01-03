# Example FastAPI Application

This is an example FastAPI application that demonstrates how to create and manage users, as well as perform operations on odd numbers.

## Features

- Create users with a name and email.
- Retrieve a list of users.
- Fetch odd numbers within a specified range.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/example_fastapi_app.git
   cd example_fastapi_app
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database and update the `DATABASE_URL` in `main.py`:

   ```python
   DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"
   ```

## Running the Application

1. Start the PostgreSQL database using Docker:

   ```bash
   docker-compose up -d
   ```

2. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

3. Access the application at `http://127.0.0.1:8000`.

## API Endpoints

### Create User

- **Endpoint**: `POST /users/`
- **Request Body**:

  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
  ```

- **Response**:

  ```json
  {
    "user_id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
  ```

### Get Users

- **Endpoint**: `GET /users/`
- **Response**:

  ```json
  [
    {
      "user_id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com"
    },
    {
      "user_id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com"
    }
  ]
  ```

### Get User by ID

- **Endpoint**: `GET /users/{user_id}`
- **Response**:

  ```json
  {
    "user_id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
  ```

### Get Odd Numbers

- **Endpoint**: `GET /odd-numbers/?start=1&end=100`
- **Response**:

  ```json
  {
    "odd_numbers": [1, 3, 5, 7, 9, ..., 99]
  }
  ```

## Running the Application with Makefile

You can use the provided Makefile to easily manage your FastAPI application. Below are the available commands:

### Commands

- **Install dependencies**:

  ```bash
  make install
  ```

  This command will create a virtual environment (if it doesn't exist) and install all required packages from `requirements.txt`.

- **Run the FastAPI application**:

  ```bash
  make run
  ```

  This command will start the FastAPI application using Uvicorn. You can access the application at `http://127.0.0.1:8000`.

- **Run tests** (if you have a test suite):

  ```bash
  make test
  ```

  This command will discover and run tests located in the `tests` directory.

- **Start Docker containers** (if using Docker):

  ```bash
  make docker-up
  ```

  This command will start the Docker containers defined in your `docker-compose.yml` file.

- **Stop Docker containers**:

  ```bash
  make docker-down
  ```

  This command will stop the running Docker containers.

- **Clean up**:

  ```bash
  make clean
  ```

  This command will remove the virtual environment.

### Note

Make sure you are in the directory where the Makefile is located before running these commands.