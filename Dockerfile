FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

RUN chown -R appuser:appuser /app

USER appuser

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
