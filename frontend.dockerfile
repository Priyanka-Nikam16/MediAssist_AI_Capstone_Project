FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements_frontend.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements_frontend.txt

# Copy project
COPY . .

# Change to App folder
WORKDIR /app/App

EXPOSE 8501

CMD ["streamlit", "run", "frontend/Chat.py", "--server.port=8501", "--server.address=0.0.0.0"]






# FROM python:3.11-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#  && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# COPY . .

# WORKDIR /app/App

# EXPOSE 8501
# CMD [
#     "streamlit",
#     "run",
#     "frontend/chat.py",
#     "--server.port=8501",
#     "--server.address=0.0.0.0"
# ]