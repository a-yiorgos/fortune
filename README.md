# Fortune & Devil's Dictionary Application

This repository consists of a backend API serving Unix fortunes and Ambrose Bierce's *The Devil's Dictionary*, along with a web front-end application to interact with it.

## Architecture

- **`backend/`**: FastAPI service listening on port 8000 (by default) that serves fortune and dictionary quotes.
- **`frontend/`**: Express web server listening on port 3000 that serves an interactive UI with "Fortune" and "Dictionary" buttons. The frontend connects to the backend via `BACKEND_URL` environment variable (defaults to `http://127.0.0.1:8000`).

---

## Backend (`backend/`)

### Features & Endpoints

- **Fortune Endpoints**:
  - `GET /fortune`: API help and fortune count.
  - `GET /fortune/random`: Random fortune quote.
  - `GET /fortune/{n}`: $n$-th fortune quote (1-indexed).
- **Devil's Dictionary Endpoints**:
  - `GET /dict`: API help and total entries count.
  - `GET /dict/lemmata`: List of all lemmata.
  - `GET /dict/random`: Random dictionary entry.
  - `GET /dict/{n}`: $n$-th entry (1-indexed).
  - `GET /dict/{letter}`: Range limits for a specific letter.
  - `GET /dict/random/{letter}`: Random entry starting with a letter.

### Local Setup & Testing

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Run tests:
```bash
cd backend
python3 -m pytest
```

### Docker Usage

```bash
cd backend
docker build -t fortune-backend .
docker run -p 8000:8000 -e PORT=8000 fortune-backend
```

---

## Frontend (`frontend/`)

### Features

- Web UI with **Fortune** and **Dictionary** buttons.
- Fetches random quotes from backend endpoints (`/fortune/random` and `/dict/random`).
- Configurable backend target via `BACKEND_URL` environment variable (defaults to `http://127.0.0.1:8000`).
- Listens on port 3000 (configurable via `PORT` environment variable).

### Local Setup

```bash
cd frontend
npm install
npm start
```

With custom backend URL:
```bash
BACKEND_URL=http://localhost:8000 npm start
```

### Docker Usage

```bash
cd frontend
docker build -t fortune-frontend .
docker run -p 3000:3000 -e BACKEND_URL=http://127.0.0.1:8000 fortune-frontend
```
