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

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

# Copy the built frontend from the previous stage to /app/frontend/dist
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Copy backend files
COPY backend/requirements.txt ./backend/
COPY backend/app ./backend/app

WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

# Create database directory
RUN mkdir -p /data

# Set environment variables
ENV DATABASE_URL=sqlite:////data/app.db
ENV PYTHONPATH=/app/backend
ENV FRONTEND_DIST_PATH=/app/frontend/dist

# Debug: Verify frontend files exist
RUN echo "DEBUG: Checking frontend dist..." && ls -la /app/frontend/dist/ && echo "Frontend verified!"

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
