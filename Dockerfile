FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip build-essential

COPY requirements.txt requirements.txt
RUN pip3 install --requirement requirements.txt

COPY api api
COPY s3 s3

ENTRYPOINT [ "gunicorn", "-w", "4", "-t", "1480", "-b", "0.0.0.0:5000", "api:create_app()" ]