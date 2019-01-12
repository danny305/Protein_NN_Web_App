FROM ubuntu:16.04

ADD NN_app/website /app/website
WORKDIR /app/website

RUN apt-get update && apt-get install -y python python-pip && pip install --upgrade pip && pip install -r requirements.txt 

ADD entrypoint.sh /app/website

CMD [ "./entrypoint.sh"]
