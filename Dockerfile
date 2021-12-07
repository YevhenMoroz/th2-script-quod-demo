FROM ubuntu:latest
RUN apt update -y && apt-get install git -y && apt-get install python3 -y && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN apt-get install pip -y

USER docker
CMD /bin/bash