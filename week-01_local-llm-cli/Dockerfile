FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y git gcc g++ libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Llama-cpp-python requires compilation with BLAS support for performance
#ENV LLAMA_CPP_LIB="auto"

# Copy all scripts
COPY . .

# Default command
CMD ["python", "cli_assistant.py"]