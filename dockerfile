# ==========================
# Base Image
# ==========================
FROM python:3.11-slim

# ==========================
# Environment Variables
# ==========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==========================
# Working Directory
# ==========================
WORKDIR /app

# ==========================
# Install System Dependencies
# ==========================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# Copy Requirements
# ==========================
COPY requirements.txt .

# ==========================
# Install Python Packages
# ==========================
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# Copy Project Files
# ==========================
COPY . .

# ==========================
# Create Required Directories
# ==========================
RUN mkdir -p \
    data \
    store \
    backend/logs

# ==========================
# Expose Ports
# ==========================
EXPOSE 8000
EXPOSE 8501

# ==========================
# Start FastAPI + Streamlit
# ==========================
CMD sh -c "\
uvicorn backend.app:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/Chat.py --server.address=0.0.0.0 --server.port=8501"