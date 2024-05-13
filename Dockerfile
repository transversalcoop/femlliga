FROM python:3.11

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY config /code/config/
COPY femlliga /code/femlliga/
COPY locale /code/locale/
COPY manage.py /code/
