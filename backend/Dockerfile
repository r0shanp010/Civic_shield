# -------------------------------------------------------------------
# CivicShield Backend Production Dockerfile
# Python 3.11 Slim with FastAPI, Uvicorn & Scikit-Learn NLP Engine
# -------------------------------------------------------------------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies (build-essential, curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK stopwords if needed
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

# Copy application source code and AI models
COPY app/ ./app/
COPY civicshield.db .
COPY civicshield_database.sql .

# Create uploads directory for evidence files
RUN mkdir -p uploads

# Expose backend port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run FastAPI backend with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
