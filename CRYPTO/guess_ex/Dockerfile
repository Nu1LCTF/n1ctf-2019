FROM ubuntu:latest
MAINTAINER i@shiki7.me

# OPTIONAL: Switch source
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/jp.archive.ubuntu.com/g" /etc/apt/sources.list

# Install dependencies
RUN apt update && apt upgrade -y
RUN apt install -y python2.7 xinetd

# Install challenge & network
RUN mkdir /challenge/
ADD ./flag /flag
ADD ./src/run.sh /challenge/run.sh
ADD ./src/guess.py /challenge/guess.py
RUN chmod +x /challenge/run.sh
RUN useradd ctf
ADD ./problem /etc/xinetd.d/

CMD ["/usr/sbin/xinetd", "-dontfork"]

