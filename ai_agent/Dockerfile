# Use Ollama as base image
FROM ollama/ollama:0.6.7

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create start script with proper Ollama configuration
RUN echo '#!/bin/bash\n\
ollama serve & \n\
sleep 5 \n\
ollama pull gemma:2b \n\
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8003\n' > /start.sh \
    && chmod +x /start.sh

EXPOSE 11434 8003

ENTRYPOINT ["/bin/bash", "/start.sh"]