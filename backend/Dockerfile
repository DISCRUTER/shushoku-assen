# syntax=docker/dockerfile:1

########## Stage 1 — build dependency venv with uv ##########
FROM python:3.13-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy lock files first so dependency layers cache independently of source
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

########## Stage 2 — runtime ##########
FROM python:3.13-slim-bookworm

# WeasyPrint system libraries (same set installed in CI workflow)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz-subset0 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system app \
    && useradd --system --gid app app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /app/.venv /app/.venv

COPY app.py celery_config.py ./
COPY application ./application
COPY templates ./templates
COPY static ./static

# instance/ holds the SQLite DB; static/reports holds generated PDFs.
# Pre-create with correct ownership so named volumes inherit it on first use.
RUN mkdir -p instance static/reports \
    && chown -R app:app /app

USER app

EXPOSE 3000

CMD ["python", "app.py"]
