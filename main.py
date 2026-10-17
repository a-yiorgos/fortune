import os
import random
from pathlib import Path
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Fortune API", description="API server serving quotes from UNIX fortunes")

FORTUNES_FILE = Path(__file__).parent / "fortunes"


def load_fortunes():
    if not FORTUNES_FILE.exists():
        return []
    with open(FORTUNES_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


fortunes_db = load_fortunes()


@app.get("/fortune")
async def get_fortune_help():
    return {
        "message": "Welcome to the Fortune API!",
        "endpoints": {
            "/fortune": "Returns this help message in JSON format",
            "/fortune/random": "Returns a random quote",
            "/fortune/{n}": "Returns the n-th quote in the database (1-indexed)",
        },
        "total_fortunes": len(fortunes_db),
    }


@app.get("/fortune/random")
async def get_random_fortune():
    if not fortunes_db:
        raise HTTPException(status_code=404, detail="No fortunes available")
    return {"fortune": random.choice(fortunes_db)}


@app.get("/fortune/{n}")
async def get_nth_fortune(n: int):
    if n < 1 or n > len(fortunes_db):
        raise HTTPException(status_code=404, detail=f"Fortune index {n} not found. Valid index range is 1 to {len(fortunes_db)}.")
    return {"id": n, "fortune": fortunes_db[n - 1]}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
