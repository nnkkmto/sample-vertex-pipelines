FROM python:3.8.10-slim-buster

COPY ./images/component/requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

ARG COMPONENT

COPY ./src/component/$COMPONENT/ ./src

WORKDIR /src
ENTRYPOINT ["python", "task.py"]