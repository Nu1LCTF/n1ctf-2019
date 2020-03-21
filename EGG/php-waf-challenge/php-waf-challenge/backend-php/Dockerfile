FROM ubuntu:18.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install tzdata
RUN apt-get -y install php
RUN apt-get -y install apache2
RUN apt-get -y install libapache2-mod-php 
RUN apt-get -y install python3-pip --fix-missing
RUN pip3 install requests
RUN pip3 install pika
RUN apt-get -y install vim

COPY cases /root/cases
COPY handler /root/handler

RUN chmod 0755 -R /var/www/html
RUN chmod 0755 -R /tmp/
RUN chmod 0755 -R /var/tmp/

COPY limit.ini /etc/php/7.2/apache2/conf.d/

WORKDIR /root/handler/

CMD service apache2 restart;sleep 20;python3 consumer.py