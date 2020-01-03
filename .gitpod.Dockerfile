FROM gitpod/workspace-mongodb
                    


# Install custom tools, runtime, etc. using apt-get
FROM gitpod/workspace-full:latest

USER root
# Setup Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

USER gitpod
# Local environment variables
# C9_* variables are temporary
ENV C9_USER="gitpod"
ENV PORT="8080"
ENV IP="0.0.0.0"
ENV C9_HOSTNAME="localhost"

# Installs MongoDB
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN sudo apt-get update \
 && sudo apt-get install -y mongodb-org \
 && sudo apt-get clean \
 && sudo rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/*
RUN sudo mkdir -p /data/db
RUN sudo chown gitpod:gitpod -R /data/db
RUN pip3 install flask
RUN pip3 install flask_pymongo
RUN pip3 install dnspython
USER root
# Switch back to root to allow IDE to load