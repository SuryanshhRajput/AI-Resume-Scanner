FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port (Railway will set PORT env var at runtime)
EXPOSE 8000

# Run the application (Railway will set PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

