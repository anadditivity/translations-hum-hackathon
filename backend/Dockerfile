FROM ghcr.io/astral-sh/uv:alpine3.23 as builder
WORKDIR /app
COPY pyproject.toml .
COPY ./src /app/src
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync
CMD ["run.sh"]
