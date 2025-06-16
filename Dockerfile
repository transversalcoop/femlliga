FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml uv.lock /code/
RUN uv sync --frozen

COPY config /code/config/
COPY femlliga /code/femlliga/
COPY locale /code/locale/
COPY manage.py /code/
