FROM node:18-alpine AS frontend-build

WORKDIR /app

# Copy frontend files
COPY frontend/package*.json ./frontend/
COPY frontend/ ./frontend/

WORKDIR /app/frontend

# Install dependencies and build
RUN npm install --production=false
RUN npm run build

# Verify build output
RUN ls -la dist/

# Backend stage
FROM python:3.10-slim

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip setuptools wheel

# Copy the built frontend from the previous stage
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Verify frontend files were copied
RUN ls -la frontend/dist/

# Copy backend files
COPY backend/requirements.txt ./backend/
COPY backend/app ./backend/app
COPY backend/alembic ./backend/alembic
COPY backend/alembic.ini ./backend/

WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

# Create database directory
RUN mkdir -p /data

# Set environment variables
ENV DATABASE_URL=sqlite:////data/app.db
ENV PYTHONPATH=/app/backend
ENV FRONTEND_DIST_PATH=/app/frontend/dist

# Expose port
EXPOSE 8000

# Run database migrations and start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
