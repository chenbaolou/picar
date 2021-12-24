#!coding:utf-8
from multiprocessing import Process, Queue
import os,time,random
import bluetooth
import math
from move import CarMove

car = CarMove()

def control_car(xy):
    xy_array = xy.split(",")

    if len(xy_array) == 2:
        car.forward(xy_array[1])
        car.turn(xy_array[0])

def proc_recv(q):
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    while True:
        print("Waiting for incoming connection...")
        client_sock, address = server_sock.accept()
        print("Accepted connection from ", str(address))
        print("Waiting for data...")
        while True:
            try:
                data = client_sock.recv(1024)
            except bluetooth.BluetoothError as e:
                break
            if not data:
                break
            print("Received data %s" %(data))
            control = data.split(";")
            if len(control) < 0:
                continue
            if control[0] == "status":
                #q.put("status")
                client_sock.send("status")
            elif control[0] == "CARCONTROL":
                if len(control) < 1:
                    continue
                control_car(control[1])

        client_sock.close()
        print("Connection closed")

    server_sock.close()

def proc_send(q):
    print('Process is reading...')
    while True:
        data = q.get(True)
        print('Get %s from queue' %data)

if __name__ == '__main__':
    q = Queue()
    
    _proc_recv = Process(target=proc_recv,args=(q,))
    _proc_send = Process(target=proc_send,args=(q,))
    
    _proc_recv.start()
    _proc_send.start()

    _proc_recv.join()
    _proc_send.join()
    
   