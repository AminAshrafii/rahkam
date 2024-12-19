FROM python:3.11-slim AS builder

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application files
COPY . .

# Stage 2: Runtime stage
FROM python:3.11-alpine

# Set work directory
WORKDIR /app

# Copy dependencies from the build stage
COPY --from=builder /install /usr/local

# Copy application files
COPY . .

# Set the entry point command
ENTRYPOINT ["python", "nginx_metrics.py"]