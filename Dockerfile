FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY debs/libssl.deb /code/
COPY debs/wkhtmltox.deb /code/
RUN apt update && apt install -y xfonts-75dpi xfonts-base
RUN dpkg -i /code/libssl.deb
RUN dpkg -i /code/wkhtmltox.deb

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml uv.lock /code/
RUN uv sync --frozen

COPY config /code/config/
COPY femlliga /code/femlliga/
COPY civitapp /code/civitapp/
COPY locale /code/locale/
COPY manage.py /code/
