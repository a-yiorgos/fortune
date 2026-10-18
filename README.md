# Fortune & Devil's Dictionary API

A lightweight FastAPI application that serves fortune quotes from the classic Research-V7 Unix fortunes file (`usr/games/lib/fortunes`) and definitions/quotes from Ambrose Bierce's *The Devil's Dictionary* (Project Gutenberg #972).

## Features

- **Fortune API**:
  - **Help Endpoint (`/fortune`)**: Returns a JSON summary of available fortune endpoints and API information.
  - **Random Quote (`/fortune/random`)**: Returns a randomly selected fortune from the dataset.
  - **N-th Quote (`/fortune/{n}`)**: Returns the 1-indexed $n$-th fortune in the dataset, or a `404 Not Found` error if $n$ is out of bounds.
- **Devil's Dictionary API (`/dict`)**:
  - **Help Endpoint (`/dict`)**: Returns a JSON summary of available dictionary endpoints.
  - **Random Dictionary Entry (`/dict/random`)**: Returns a randomly selected quote/definition from *The Devil's Dictionary*.
  - **N-th Entry (`/dict/{n}`)**: Returns the 1-indexed $n$-th quote/definition.
  - **Letter Sequence Limits (`/dict/{letter}`)**: Returns sequence number limits (`min_id` and `max_id`) for quotes under a specific letter (e.g. `/dict/a` or `/dict/A`).
  - **Random Entry by Letter (`/dict/random/{letter}`)**: Returns a random quote starting with the specified letter (e.g. `/dict/random/a`).
- **Configurable Port**: Listens on the port specified by the `PORT` environment variable (defaults to `8000`).
- **Rootless Container**: Includes a Dockerfile designed for rootless container runtimes.

## API Endpoints

### Fortune Endpoints

| Endpoint | Method | Description | Response Example |
|---|---|---|---|
| `/fortune` | GET | Returns API help message and total fortune count | `{"message": "Welcome...", "endpoints": {...}, "total_fortunes": 141}` |
| `/fortune/random` | GET | Returns a random fortune quote | `{"fortune": "Words must be weighed, not counted."}` |
| `/fortune/{n}` | GET | Returns the $n$-th fortune quote (1-indexed) | `{"id": 1, "fortune": "Some men are discovered; others are found out."}` |

### Devil's Dictionary Endpoints

| Endpoint | Method | Description | Response Example |
|---|---|---|---|
| `/dict` | GET | Returns API help message and total quote count | `{"message": "Welcome...", "endpoints": {...}, "total_quotes": 995}` |
| `/dict/random` | GET | Returns a random quote | `{"id": 12, "lemma": "ABNORMAL", "definition": "ABNORMAL, adj. Not conforming..."}` |
| `/dict/{n}` | GET | Returns the $n$-th quote (1-indexed) | `{"id": 1, "lemma": "ABASEMENT", "definition": "ABASEMENT, n. A decent..."}` |
| `/dict/{letter}` | GET | Returns range limits for the given letter | `{"letter": "a", "min_id": 1, "max_id": 83}` |
| `/dict/random/{letter}` | GET | Returns a random quote for the given letter | `{"id": 5, "lemma": "ABILITY", "definition": "ABILITY, n. The natural..."}` |

## Local Setup

### Prerequisites

- Python 3.10+

### Installation & Execution

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server using Python or uvicorn:
   ```bash
   python main.py
   ```
   Or explicitly set `PORT`:
   ```bash
   PORT=8080 python main.py
   ```

3. Run tests:
   ```bash
   python3 -m pytest
   ```

## Docker Usage

Build and run the rootless container:

```bash
docker build -t fortune-api .
docker run -p 8000:8000 -e PORT=8000 fortune-api
```
