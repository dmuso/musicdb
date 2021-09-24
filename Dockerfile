FROM python:3-slim

RUN python -m pip install Django

RUN mkdir -p /app
WORKDIR /app
