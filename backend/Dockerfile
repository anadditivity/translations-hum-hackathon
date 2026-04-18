# syntax=docker.io/docker/dockerfile:1.7-labs

# Base image
FROM python:3.14.3
COPY --from=ghcr.io/astral-sh/uv:0.8.12 /uv /uvx /bin/

# Copy the project into the image
ADD --exclude=db-data . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["./run.sh"] 
CMD ["--port", "8000", "--host", "0.0.0.0"]
