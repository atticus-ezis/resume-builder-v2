# Build stage: use uv's Python image so uv is pre-installed (avoids COPY path issues)
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Install build dependencies (for WeasyPrint etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./
ENV UV_NO_DEV=1
# Install dependencies only first (better layer caching)
RUN uv sync --no-install-project
COPY . .
RUN uv sync

# Runtime stage (same registry as builder to avoid Docker Hub timeouts)
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Runtime dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libharfbuzz-subset0 \
    libjpeg62-turbo \
    libopenjp2-7 \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Use the venv from builder (uv sync creates .venv, not system site-packages)
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY . .
RUN chmod +x /app/entrypoint.sh /app/entrypoint-prod.sh
RUN chmod +x /app/entrypoint-prod.sh

EXPOSE 8000
# Use 1 worker on memory-limited hosts (e.g. Render); override with GUNICORN_WORKERS=3 if needed
ENV GUNICORN_WORKERS=1
# Render sets PORT=10000; entrypoint reads PORT and binds so the port scan succeeds
ENTRYPOINT ["/app/entrypoint.sh"]

