FROM ubuntu:latest
RUN apt update -y && apt-get install git -y && apt-get install python3 -y
RUN python3 --version
RUN apt-get install pip -y
RUN virtualenv enviroment_name -p python3
RUN source enviroment_name/bin/activate