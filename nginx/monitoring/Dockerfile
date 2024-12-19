# Multistage Dockerfile for Python Application

# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install  -r requirements.txt

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

# Expose necessary ports (optional if you are running an HTTP server or similar)
EXPOSE 9145

# Set the entry point command
ENTRYPOINT ["python", "app.py"]
