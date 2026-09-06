FROM ghcr.io/astral-sh/uv:0.11.0 AS uv
FROM python:3.12-slim
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /application
COPY pyproject.toml uv.lock ./
COPY backend ./backend
COPY packages ./packages
RUN uv sync --locked --all-packages --no-dev
COPY database ./database
COPY data ./data
COPY spec/database ./spec/database
COPY tools/local_database.py tools/start_database.py ./tools/
ENV PATH="/application/.venv/bin:$PATH" PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
