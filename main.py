import os
import random
from pathlib import Path
from fastapi import FastAPI, HTTPException
from parser import parse_devils_dictionary

app = FastAPI(title="Fortune and Devil's Dictionary API", description="API server serving quotes from UNIX fortunes and The Devil's Dictionary")

FORTUNES_FILE = Path(__file__).parent / "fortunes"


def load_fortunes():
    if not FORTUNES_FILE.exists():
        return []
    with open(FORTUNES_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


fortunes_db = load_fortunes()
dict_db, dict_letter_limits = parse_devils_dictionary()


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


# Devil's Dictionary Endpoints


@app.get("/dict")
async def get_dict_help():
    return {
        "message": "Welcome to The Devil's Dictionary API!",
        "endpoints": {
            "/dict": "Returns this help message in JSON format",
            "/dict/random": "Returns a random quote from The Devil's Dictionary",
            "/dict/{n}": "Returns the n-th quote in the dictionary (1-indexed)",
            "/dict/{letter}": "Returns sequence number limits (min_id and max_id) for the given letter (e.g. /dict/a)",
            "/dict/random/{letter}": "Returns a random quote starting with the given letter",
        },
        "total_quotes": len(dict_db),
    }


@app.get("/dict/random")
async def get_random_dict_quote():
    if not dict_db:
        raise HTTPException(status_code=404, detail="No dictionary quotes available")
    rand_idx = random.randint(1, len(dict_db))
    entry = dict_db[rand_idx - 1]
    return {
        "id": rand_idx,
        "lemma": entry["lemma"],
        "definition": entry["definition"],
    }


@app.get("/dict/random/{letter}")
async def get_random_dict_quote_by_letter(letter: str):
    let = letter.lower()
    if let not in dict_letter_limits:
        raise HTTPException(status_code=404, detail=f"Letter '{letter}' not found or has no entries.")
    limits = dict_letter_limits[let]
    rand_idx = random.randint(limits["min_id"], limits["max_id"])
    entry = dict_db[rand_idx - 1]
    return {
        "id": rand_idx,
        "lemma": entry["lemma"],
        "definition": entry["definition"],
    }


@app.get("/dict/{param}")
async def get_dict_by_param(param: str):
    # If param is an integer, handle as n-th entry
    if param.isdigit():
        n = int(param)
        if n < 1 or n > len(dict_db):
            raise HTTPException(
                status_code=404,
                detail=f"Dictionary index {n} not found. Valid index range is 1 to {len(dict_db)}.",
            )
        entry = dict_db[n - 1]
        return {
            "id": n,
            "lemma": entry["lemma"],
            "definition": entry["definition"],
        }

    # Otherwise, handle as letter parameter
    if len(param) == 1 and param.isalpha():
        let = param.lower()
        if let in dict_letter_limits:
            limits = dict_letter_limits[let]
            return {
                "letter": let,
                "min_id": limits["min_id"],
                "max_id": limits["max_id"],
            }

    raise HTTPException(status_code=404, detail=f"Invalid parameter '{param}'. Must be an index (1 to {len(dict_db)}) or a single letter (a-z).")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
