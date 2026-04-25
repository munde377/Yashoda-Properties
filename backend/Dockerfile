FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]