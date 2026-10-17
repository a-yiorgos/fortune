# Fortune API

A lightweight FastAPI application that serves fortune quotes from the classic Research-V7 Unix fortunes file (`usr/games/lib/fortunes`).

## Features

- **Help Endpoint (`/fortune`)**: Returns a JSON summary of available endpoints and API information.
- **Random Quote (`/fortune/random`)**: Returns a randomly selected fortune from the dataset.
- **N-th Quote (`/fortune/{n}`)**: Returns the 1-indexed $n$-th fortune in the dataset, or a `404 Not Found` error if $n$ is out of bounds.
- **Configurable Port**: Listens on the port specified by the `PORT` environment variable (defaults to `8000`).
- **Rootless Container**: Includes a Dockerfile designed for rootless container runtimes.

## API Endpoints

| Endpoint | Method | Description | Response Example |
|---|---|---|---|
| `/fortune` | GET | Returns API help message and total fortune count | `{"message": "Welcome...", "endpoints": {...}, "total_fortunes": 141}` |
| `/fortune/random` | GET | Returns a random fortune quote | `{"fortune": "Words must be weighed, not counted."}` |
| `/fortune/{n}` | GET | Returns the $n$-th fortune quote (1-indexed) | `{"id": 1, "fortune": "Some men are discovered; others are found out."}` |

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
   pytest
   ```

## Docker Usage

Build and run the rootless container:

```bash
docker build -t fortune-api .
docker run -p 8000:8000 -e PORT=8000 fortune-api
```
