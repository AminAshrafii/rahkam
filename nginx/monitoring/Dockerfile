FROM python:3.11-slim

# Set work directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set the entry point command
ENTRYPOINT ["python", "app.py"]
