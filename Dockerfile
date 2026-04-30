FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set PYTHONPATH to include the current directory so 'backend' is findable
ENV PYTHONPATH=/app

# Default command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
