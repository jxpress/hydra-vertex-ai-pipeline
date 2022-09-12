FROM python:3.8-slim
WORKDIR /root


RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && pip install poetry


COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . .