# Stage 1: Build React Frontend
FROM node:18 as build-step
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# (Assuming output is /app/dist or /app/build)

# Stage 2: Python Backend
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .
[cite_start]RUN pip install --no-cache-dir -r requirements.txt [cite: 3]

# Copy the Backend Code
COPY backend ./backend
COPY main.py .

# Copy the built Frontend from Stage 1
COPY --from=build-step /app/dist ./frontend/dist

[cite_start]EXPOSE 8080 [cite: 4]

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
