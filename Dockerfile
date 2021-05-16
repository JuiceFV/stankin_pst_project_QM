FROM python:3.8

RUN apt-get -q update && apt-get -y install netcat

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN cat ./docker_config.yaml > ./application/config.yaml

RUN curl -OL https://raw.githubusercontent.com/mrako/wait-for/master/wait-for && chmod +x wait-for

RUN pip install -r requirements.txt
