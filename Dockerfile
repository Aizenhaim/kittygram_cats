FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run migrations and start gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn kittygram2.wsgi:application --bind 0.0.0.0:8001 --workers 2"]
