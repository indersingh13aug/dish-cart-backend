FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . /app
# COPY .env.production .env  
# default

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Start app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]