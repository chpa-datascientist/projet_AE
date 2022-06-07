FROM ubuntu:focal-20220426
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install python3-pip -y && apt-get install libglib2.0-0 libgl1 libsm6 libxrender1 libxext6 -y

COPY ./app/requirements.txt /home/ubuntu/projet_AE/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/ubuntu/projet_AE/requirements.txt

RUN python3 -m spacy download fr_core_news_lg

COPY ./app /home/ubuntu/projet_AE/app

RUN mkdir -p /home/ubuntu/projet_AE/app/files
RUN mkdir -p /home/ubuntu/projet_AE/app/image_user
RUN mkdir -p /home/ubuntu/projet_AE/app/images_project
COPY ./app/images_project /home/ubuntu/projet_AE/app/images_project

WORKDIR /home/ubuntu/projet_AE/app

EXPOSE 80

CMD uvicorn main_fastapi:app --host 0.0.0.0 --port 80 
