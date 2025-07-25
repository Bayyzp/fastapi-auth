# Auth API with FastAPI & MySQL (Dockerized)

## 🚀 How to Run

1. Build and start the containers:

```bash
docker-compose up --build
```

2. Visit the FastAPI docs:

[http://localhost:8000/docs](http://localhost:8000/docs)

## 📦 Services

- `fastapi` — runs the FastAPI backend
- `db` — MySQL 8.0 with default credentials

## 🔐 MySQL Credentials

```
HOST: db
PORT: 3306
USER: authuser
PASSWORD: authpass
DATABASE: authdb
```

Ensure your app reads DB config from `.env` like:

```env
DB_HOST=db
DB_PORT=3306
DB_USER=authuser
DB_PASSWORD=authpass
DB_NAME=authdb
```

## 📁 File Structure

```
auth_api_final/
├── app/
├── .env
├── requirements.txt
├── start.sh
├── Dockerfile
├── docker-compose.yml
└── README.md
```