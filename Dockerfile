# Stage 1: Build React Frontend
FROM node:18 as build-step
WORKDIR /app
COPY frontend/package*.json ./
COPY frontend/ ./frontend/ 
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Stage 2: Python Backend
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend ./backend
COPY main.py .
COPY data ./data 

# Copy the built Frontend from Stage 1
COPY --from=build-step /app/frontend/dist ./frontend/dist

EXPOSE 8080
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
