# dockerfile for python with flask dependency
FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
VOLUME /app/data

USER 1000

# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# docker build -t coucou619/polldance:v3 .
# docker run -p 5000:5000 coucou619/polldance:v3
# docker push coucou619/polldance:v3
