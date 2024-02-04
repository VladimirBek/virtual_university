FROM python:3

WORKDIR /drf

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .