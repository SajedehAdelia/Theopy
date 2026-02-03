FROM python:3.11-slim

# --- SYSTEM DEPENDENCIES ---
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    libc-dev \
    python3-dev \
    portaudio19-dev \
    libasound2-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- PYTHON DEPENDENCIES ---
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- SOURCE CODE ---
COPY . .

# --- CONFIGURATION ---
ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "src/app.py"]