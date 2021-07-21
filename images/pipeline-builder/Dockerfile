FROM python:3.8.10-slim-buster

COPY ./images/pipeline-builder/requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

ARG PROJECT_ID
ENV PROJECT_ID=$PROJECT_ID

