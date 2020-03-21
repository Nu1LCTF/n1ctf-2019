# -*- coding: utf-8 -*-
import pika
import sys
import json

class MessageQ():

    def __init__(self,host,username,password,queue):
        self.username = username
        self.password = password
        self.credential = pika.PlainCredentials(username,password)
        self.host = host
        self.queue = queue


    def send(self,mess):

        mess = json.dumps(mess)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=self.credential,heartbeat=0))
        self.chanel = self.s_conn.channel()
        self.chanel.queue_declare(queue=self.queue,durable=True)
        self.chanel.basic_publish(exchange='',properties=pika.BasicProperties(
                         delivery_mode = 2,
                        priority = 5,
                      ),routing_key=self.queue,body=mess)
        self.s_conn.close()
        return

    def send_vim(self,mess):
        mess = json.dumps(mess)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=self.credential,heartbeat=0))
        self.chanel = self.s_conn.channel()
        self.chanel.queue_declare(queue=self.queue,durable=True)
        self.chanel.basic_publish(exchange='', properties=pika.BasicProperties(
            delivery_mode=2,
            priority = 1,
        ), routing_key=self.queue, body=mess)
        self.s_conn.close()
        return

    def recv(self):
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=self.credential,heartbeat=0))
        self.chanel = self.s_conn.channel()
        self.chanel.queue_declare(queue=self.queue,durable=True)
        while True:
            recvmess = self.chanel.basic_get(self.queue,auto_ack=True)[2]
            if recvmess == None:
                continue
            else:
                break
        self.s_conn.close()
        return json.loads(str(recvmess, encoding='utf8'))



    def clear(self):
        return self.chanel.queue_delete(self.queue)
