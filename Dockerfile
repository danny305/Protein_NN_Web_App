FROM ubuntu:16.04

ADD ./web_app /web_app
WORKDIR web_app/

#RUN apt-get update && apt-get install -y python python-pip && pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y python python-pip && pip install -r requirements.txt

# ADD entrypoint.sh /app

CMD [ "./entrypoint.sh"]
