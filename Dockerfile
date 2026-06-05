# Stage 1: Build the React Application
FROM node:20 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Setup Python Backend and Serve
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

# Hugging Face Spaces require the application to listen on port 7860
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
