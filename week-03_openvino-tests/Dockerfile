FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (combine RUNs for layer efficiency)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements files first for better build caching
COPY requirements.txt .
COPY requirements_cpu.txt .

# Install Python dependencies in a single RUN for speed and smaller image
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -r requirements_cpu.txt && \
    pip install --no-cache-dir notebook

# Copy all scripts and notebooks
COPY . .

EXPOSE 8888

# Create a non-root user and set permissions
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Default command: run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''"]
