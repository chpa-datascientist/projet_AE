FROM ubuntu:focal-20220426
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install python3-pip -y && pip3 install requests 

COPY . /app

WORKDIR /app

CMD python3 test_API_ML.py

