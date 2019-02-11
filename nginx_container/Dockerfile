FROM nginx:latest
LABEL maintainer="danny.diaz@utexas.edu"

SHELL ["/bin/bash", "-c"]

# Remove default nginx site configuration
#RUN rm /etc/nginx/sites-enabled/default
# Copy my nn_web_app nginx config files 
COPY ./nginx_config/* /etc/nginx/sites-available/
# Create sym-link from sites-enabled to sites-available
#RUN ln -s /etc/nginx/sites-available/nn_app /etc/nginx/sites-enabled/nn_app

EXPOSE 80 443 8000 



ENTRYPOINT ['sudo', 'systemd', 'start', 'nginx']
