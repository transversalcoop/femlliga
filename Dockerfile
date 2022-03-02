FROM python:3.9

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY config /code/config/
COPY femlliga /code/femlliga/
COPY manage.py /code/
