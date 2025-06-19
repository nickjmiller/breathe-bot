FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# Copy the project into the image
COPY . /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libffi-dev \
        libnacl-dev \
    && rm -rf /var/lib/apt/lists/*

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked --compile-bytecode

CMD ["uv", "run", "main.py"]