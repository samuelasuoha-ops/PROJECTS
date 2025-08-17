# Microservices API with Flask, MongoDB & Docker

This is a simple RESTful API built with **Flask**, using **MongoDB** as the database, and containerized with **Docker**.

## Features
- Add users (POST /api/users)
- Retrieve all users (GET /api/users)
- MongoDB persistence
- Containerized with Docker & docker-compose

## Tech Stack
- Python (Flask)
- MongoDB
- Docker / Docker Compose
- REST APIs (tested with Postman)

## Run Locally (Docker)
```bash
git clone https://github.com/YOUR-USERNAME/microservices-api.git
cd microservices-api
docker-compose up --build
```

The API will be available at `http://localhost:5000/api/users`

## Example Requests
### Add User
```bash
POST /api/users
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Get Users
```bash
GET /api/users
```
