FROM python:3.9.4
COPY ./log_config.conf /var/th2/config/
RUN apt-get update
RUN apt-get install xmlstarlet
ARG USER=docker
ARG UID=50161
ARG GID=50161
# default password for user
ARG PW=docker
# Using unencrypted password/ specifying password
RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | chpasswd