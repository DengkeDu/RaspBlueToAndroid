#!/usr/bin/python
from bluetooth import *
import subprocess
from megapi import *
import signal
import sys

def signal_handler(signal,frame):
    print "Ctrl+C"
    server_sock.close()
    sys.exit(0)

bot = MegaPi()
bot.start("/dev/ttyS0")
signal.signal(signal.SIGINT,signal_handler)

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

while True:
    client_sock,client_info = server_sock.accept()
    print "connect to:"
    print client_info
    try:
        while True:
            data=client_sock.recv(1024)
            if not data:
                break
            if data == "left":
                bot.motorRun(1,0)
                bot.motorRun(2,25)
            if data == "right":
                bot.motorRun(1,25)
                bot.motorRun(2,0)
            if data == "forward":
                bot.motorRun(1,25)
                bot.motorRun(2,25)
            if data == "back":
                bot.motorRun(1,-25)
                bot.motorRun(2,-25)
            if data == "dianjistop":
                bot.motorRun(1,0)
                bot.motorRun(2,0)
            print data
    except:
        print "Closing socket" 
        client_sock.close()
        print "close one connection!"
        print "prepare to start other connection!"

server_sock.close()
       
