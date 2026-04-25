FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# IMPORTANT FIX
RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]