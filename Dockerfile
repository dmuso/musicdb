FROM python:3-slim

RUN python -m pip install Django pillow

RUN mkdir -p /app
WORKDIR /app

COPY . .
