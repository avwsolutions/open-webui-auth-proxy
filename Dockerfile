FROM python:3.13-slim

# Best practices when running Python containers (like making use of slim type)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Create a non-root user with no home
RUN groupadd appuser -g 1001 \
    && useradd appuser -u 1001 -g 1001 -M

# Install system dependencies for troubleshooting (if needed)
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Ensure perms are set correctly
RUN chown -R appuser:appuser /app

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
