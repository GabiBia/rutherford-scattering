# syntax=docker/dockerfile:1

FROM docker.io/python:3.9

ADD . /app
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD gunicorn --threads=2 --bind 0.0.0.0:5000 rutherford-scattering:app
# CMD python3 rutherford-scattering.py