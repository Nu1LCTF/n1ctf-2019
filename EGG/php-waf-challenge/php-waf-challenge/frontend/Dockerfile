FROM ubuntu:18.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y python3-pip --fix-missing
RUN pip3 install flask
RUN pip3 install pika
RUN pip3 install wtforms
RUN pip3 install flask_wtf
RUN pip3 install pymysql
RUN pip3 install requests

COPY app /root/app
WORKDIR /root/app

CMD sleep 25 ;(nohup python3 update_rank.py &);python3 producer.py