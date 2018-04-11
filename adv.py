#!/usr/bin/python

from bluetooth import *
import subprocess
import signal
import sys
import multiprocessing as mp
import time
# from megapi import *
flag = 1

def rec(client_sock):
    while True:
        time.sleep(0.5)
        try:
            if client_sock.getpeername()[0]:
                client_sock.send("ddk")
        except:
            print "client_sock close."
            break

def signal_handler(signal,frame):
    print "Ctrl+C"
    server_sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

# bot = MegaPi()
# bot.start("/dev/ttyS0")

cmd = "sudo hciconfig hci0 piscan"
subprocess.check_output(cmd, shell=True)
print "init"
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
other = server_sock.getsockname()[0]
len_sockname = len(server_sock.getsockname())
    
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    
advertise_service(server_sock, "AquaPiServer",
        service_id = uuid,
        service_classes = [uuid,SERIAL_PORT_CLASS],
        profiles = [ SERIAL_PORT_PROFILE ])
print "advertise service"

value = mp.Value('i',1)
while True:
    print "Head"
    value.value = 1
    client_sock,client_info = server_sock.accept()
    p = mp.Process(target=rec,args=(client_sock,))
    p.start()
    print "connect to:"
    print client_info
    try:
        while True:
            data=client_sock.recv(1024)
            if not data:
                break
            if data=="over":
                p.terminate()
                client_sock.close()
            print data
    except:
        client_sock.close()
server_sock.close()
       
