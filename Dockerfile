# BowieGame Flask Application Dockerfile
FROM python:3.12-alpine

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    musl-dev \
    linux-headers \
    python3-dev \
    sqlite \
    sqlite-dev \
    openssl \
    openssl-dev \
    libffi-dev

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/flask_session \
    && mkdir -p /app/actualdb \
    && mkdir -p /var/log

# Set up database permissions
RUN chmod 755 /app && \
    chmod 644 bowiegame.db || true && \
    chmod 755 /app/flask_session && \
    chmod 755 /app/actualdb

# Create a non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -S -D -H -u 1001 -s /sbin/nologin -G appgroup appuser

# Change ownership of app directory
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/', timeout=5)" || exit 1

# Copy gunicorn configuration
COPY gunicorn.conf.py .

# Start the Flask application with Gunicorn and SocketIO support
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]