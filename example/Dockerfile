# Designed to be run as 
# 
# docker run -it -p 8000:8000 jupyterhub/oauthenticator

FROM jupyterhub/jupyterhub

MAINTAINER Project Jupyter <ipython-dev@scipy.org>

# Install oauthenticator from git
RUN python3 -m pip install git+https://github.com/luisfdez/oauthenticator.git@5c36617f67935634167edcc42fee61e15453f0d9

# Install the Kubernetes Spawner
RUN pip install git+https://github.com/jupyterhub/kubespawner.git

# Create oauthenticator directory and put necessary files in it
RUN mkdir /srv/oauthenticator
WORKDIR /srv/oauthenticator
ENV OAUTHENTICATOR_DIR /srv/oauthenticator
ADD jupyterhub_config.py jupyterhub_config.py
#ADD addusers.sh /srv/oauthenticator/addusers.sh
#ADD userlist /srv/oauthenticator/userlist
#ADD ssl /srv/oauthenticator/ssl
RUN chmod 700 /srv/oauthenticator

#RUN ["sh", "/srv/oauthenticator/addusers.sh"]
