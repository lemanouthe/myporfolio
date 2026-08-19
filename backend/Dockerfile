# Single image serving both the Django API and the compiled Vue SPA.
# Build context is the repo root (see docker-compose.yml) so both apps are visible.

# --- Stage 1: build the Vue front ---
FROM node:20-alpine AS front
WORKDIR /front
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build         # outputs /front/dist (base=/static/ in prod)

# --- Stage 2: Django runtime ---
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
# Vue build -> served by Django/WhiteNoise (STATICFILES_DIRS + TEMPLATES DIRS)
COPY --from=front /front/dist ./frontend_build

# Run as the non-root uid used on the server (owns ./static, ./media, ./logs).
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chmod +x start.sh \
    && chown -R 1000:1000 /app
USER 1000:1000

EXPOSE 8010
CMD ["./start.sh"]
