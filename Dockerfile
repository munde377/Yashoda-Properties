# Frontend build stage
FROM node:18 AS frontend-build

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

# Install build tools and Node.js for potential frontend building
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

RUN python -m pip install --upgrade pip setuptools wheel

# Copy the built frontend from the previous stage
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Also mirror the frontend build to /frontend/dist for deployment compatibility
RUN mkdir -p /frontend/dist && cp -r /app/frontend/dist/* /frontend/dist/ || true

# Verify frontend files were copied
RUN pwd
RUN ls -la /app
RUN ls -la /app/frontend
RUN ls -la /app/frontend/dist || echo "/app/frontend/dist not found!"
RUN ls -la /frontend/dist || echo "/frontend/dist not found!"

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
ENV FRONTEND_DIST_PATH=/frontend/dist

# Expose port
EXPOSE 8000

# Run database migrations and start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
