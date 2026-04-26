FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip

# Install psycopg2 explicitly
RUN pip install psycopg2-binary

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]