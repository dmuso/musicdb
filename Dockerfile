FROM python:3-slim

RUN apt-get -u update
RUN apt-get -y install python3-dev libpq-dev build-essential

RUN python -m pip install Django pillow
RUN python -m pip install psycopg2

RUN mkdir -p /app
WORKDIR /app

COPY . .

CMD python manage.py runserver 0.0.0.0:8080
