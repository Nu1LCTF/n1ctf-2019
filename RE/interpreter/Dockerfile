FROM ubuntu:latest
MAINTAINER i@shiki7.me

# OPTIONAL: Switch source
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/jp.archive.ubuntu.com/g" /etc/apt/sources.list

# Install dependency
RUN apt update && apt upgrade -y
RUN apt install -y curl xinetd libtinfo-dev build-essential python2.7
RUN curl -sSL https://get.haskellstack.org/ | sh

# Install challenge
RUN mkdir /challenge/
COPY ./server /challenge/server
ADD ./pow.py /challenge/
ADD ./run.sh /challenge/
RUN chmod +x /challenge/run.sh
RUN cd /challenge/server && stack build 

# Setup network
ADD ./problem /etc/xinetd.d/

CMD ["/usr/sbin/xinetd", "-dontfork"]

