# dockerfile for python with flask dependency
FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
VOLUME /app/data

USER 1000

CMD ["flask", "run", "--host=0.0.0.0"]


# docker build -t coucou619/polldance:v1 .
