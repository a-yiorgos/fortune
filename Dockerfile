FROM python:3.12-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" --uid 10001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fortunes main.py ./

USER appuser

ENV PORT=8000
EXPOSE $PORT

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
