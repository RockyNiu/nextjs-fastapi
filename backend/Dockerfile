FROM python:3.13.2

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the project requirements
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync --frozen --no-cache --no-dev

# Copy the rest of the application
COPY . /app

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]