# Stage 1: Build React Frontend
FROM node:18 as build-step
WORKDIR /app

# 1. Copy package.json first (better caching)
COPY frontend/package*.json ./
RUN npm install

# 2. Copy the rest of the frontend code
COPY frontend/ .
RUN npm run build

# Stage 2: Python Backend
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 3. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Backend Code
COPY backend ./backend
COPY main.py .
COPY data ./data

# 5. Copy the built Frontend from Stage 1
# We move the 'dist' folder to exactly where main.py expects it
COPY --from=build-step /app/dist ./frontend/dist

EXPOSE 8080
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
