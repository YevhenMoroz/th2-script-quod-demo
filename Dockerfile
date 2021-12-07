FROM ubuntu:latest
RUN apt update -y && apt-get install git -y && apt-get install python3 -y
RUN apt-get install pip -y
