FROM ubuntu:latest
RUN apk add git
RUN apk add python3
RUN python3 -m ensurepip --upgrade