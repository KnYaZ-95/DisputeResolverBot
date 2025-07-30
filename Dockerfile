FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /bot

# Enable bytecode compilation
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/bot/.venv/bin:$PATH"

# Install the project's dependencies using settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-dev

# Installing separately from its dependencies allows optimal layer caching
COPY . /bot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

ENTRYPOINT ["/bot/entrypoint.sh"]

CMD ["uv", "run", "bot.py"]

