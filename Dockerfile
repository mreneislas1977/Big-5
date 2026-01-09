# Use Python as the base image
FROM python:3.9-slim

# ESSENTIAL: Ensures logs are flushed immediately to Cloud Logging
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (Documentary only, helpful for local viewing)
EXPOSE 8080

# Start the application
# Using shell form to support the $PORT environment variable if Cloud Run changes it
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
