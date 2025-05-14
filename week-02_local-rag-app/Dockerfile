FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ libopenblas-dev \
    tesseract-ocr \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Llama-cpp-python requires compilation with BLAS support for performance
# ENV LLAMA_CPP_LIB="auto"

ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages:/workspaces/generative-ai-practice/week-02_local-rag-app:/app

# Copy all scripts
COPY . .

EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Default command
CMD ["python", "cli/main.py", "chat"]
