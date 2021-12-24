#!coding:utf-8
from multiprocessing import Process, Queue
import os,time,random
import bluetooth

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
        total = 0
        while True:
            try:
                data = client_sock.recv(1024)
            except bluetooth.BluetoothError as e:
                break
            if not data:
                break
            total += len(data)
            print("Received data %s, lenthth %d" %(data, total))
            if data == "status":
                q.put("status")

        client_sock.close()
        print("Connection closed")

    server_sock.close()

def proc_send(q):
    print('Process is reading...')
    # Create the client socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    #sock.connect((address, 1))
    while True:
        data = q.get(True)
        print('Get %s from queue' %data)
        if not sock.connected:
             sock.connect((address, 1))
        sock.send(data)

if __name__ == '__main__':
    q = Queue()

    _proc_recv = Process(target=proc_recv,args=(q,))
    _proc_send = Process(target=proc_send,args=(q,))
    
    _proc_recv.start()
    _proc_send.start()

    _proc_recv.join()
    _proc_send.join()
   