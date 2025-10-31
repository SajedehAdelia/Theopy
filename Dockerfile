FROM python:3.11-slim

# Install system dependencies needed to build PyAudio
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    portaudio19-dev \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Start the app
CMD ["python", "speech_to_text.py"]
