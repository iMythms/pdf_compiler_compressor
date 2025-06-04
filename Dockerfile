# Use Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils build-essential libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]