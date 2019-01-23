FROM ubuntu:16.04

#RUN apt-get update && apt-get install -y python python-pip && pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y python python-pip gunicorn

ADD ./web_app /web_app
WORKDIR web_app/

RUN pip install -r requirements.txt
#RUN /bin/bash -c "source flask_env.sh -P"

# ADD entrypoint.sh /app
EXPOSE 8000
CMD [ "./entrypoint.sh"]

#CMD [ "gunicorn", "--bind", "127.0.0.1:5000", "wsgi:app"]