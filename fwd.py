
import random
import sys
from socket import  *
import pygame as pg
import json
import threading

from socket import  *
tcp_server = socket(AF_INET,SOCK_STREAM)
# tcp_server.setsockopt(socket.SQL_SOCKET,socket.SO_REUSEADDR,True)
#绑定ip，port
#这里ip默认本机
address = ('',8000)
tcp_server.bind(address)
tcp_server.listen(128)
dev_list=list()

count=0
def dev_handle(data):
    for dev in dev_list:

        dev.send(data.encode())
def randomshu():
    number = random.randint(1,2)
    for dev in dev_list:
        number=abs(number-1)
        dev.send(str(number).encode())
def messge_handle(tcp_client,tcp_client_ip):
    global count
    while True:
        try:
            recv_data=tcp_client.recv(4096)
            if recv_data:
                recv_data=recv_data.decode()
                if recv_data=="okok":
                    dev_list.append(tcp_client)
                if recv_data=="exit":
                    dev_list.remove(tcp_client)
                    dev_handle("dfexit")
                    count=0
                else:
                    print("kjsd")
                    if recv_data=="wait":
                       count=count+1
                    if count==2:
                        randomshu()
                        count=0
                        continue
                    dev_handle(recv_data)
        except Exception as e:
           print(str(tcp_client_ip)+str(e))
           break

if __name__=="__main__":
      while True:

          client,client_ip=tcp_server.accept()
          client.settimeout(120)
          print(str(client_ip)+"接入")
          thd=threading.Thread(target=messge_handle,args=(client,client_ip))
          thd.setDaemon = True
          thd.start()
