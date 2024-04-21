FROM python:3.11.4 AS dependencies

WORKDIR /tmp
COPY pyproject.toml poetry.lock* /tmp/
RUN pip install poetry && poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11.4 AS base

WORKDIR /app
COPY --from=dependencies /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]