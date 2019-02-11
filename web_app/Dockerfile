FROM ubuntu:16.04

LABEL maintainer="danny.diaz@utexas.edu"

#RUN apt-get update && apt-get install -y python python-pip && pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y python python-pip gunicorn
SHELL ["/bin/bash", "-c"]

ADD . /web_app
WORKDIR web_app/

RUN pip install -r requirements.txt
#RUN /bin/bash -c "source flask_env.sh -P"

# ADD entrypoint.sh /app
EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh"]

#CMD [ "gunicorn", "--bind", "127.0.0.1:5000", "wsgi:app"]
