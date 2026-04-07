# SnapMap - Backend

This is the FastAPI backend for the SnapMap project. It serves the API, handles auth, and talks to MongoDB and Cloudinary.

> [!IMPORTANT]
> This repository is a Git Submodule. It is part of the larger SnapMap project.
> To run the complete application (Backend + Frontend + Database) with a single command, please refer to the [SnapMap](https://github.com/szemerics/snapmap) Parent Repository.

## Installation

Copy the example env file and fill in real values (JWT and Cloudinary). For local MongoDB without Docker, set `MONGODB_URI` to your connection string (for example after you connect with `mongosh`).

```bash
cp .env.example .env
```

### With Docker

Build and start the API and MongoDB (from this folder, the same folder as `docker-compose.yml`):

```bash
docker compose up --build
```

Then open: http://localhost:8000

Stop containers:

```bash
docker compose down
```

To wipe the database volume and start clean:

```bash
docker compose down -v
```

### Without Docker (Local Development)

#### Prerequisites

- Python 3.13
- MongoDB running locally (or a `MONGODB_URI` you can use)

Create a virtual environment and install dependencies:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the initialization script once (sample data / setup):

```bash
python src/app/utils/init/create_init_state.py
```

Start the dev server:

```bash
fastapi dev src/main.py
```
