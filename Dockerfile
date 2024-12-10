FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR document-management
COPY requirements.txt src /document-management/
RUN pip install --no-cache-dir -r requirements.txt