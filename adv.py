from bluetooth import *
import subprocess
from megapi import *

bot = MegaPi()
bot.start("/dev/ttyS0")

cmd = "sudo hciconfig hci0 piscan"
subprocess.check_output(cmd, shell=True)
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

client_sock,client_info = server_sock.accept()
print client_info
while True:
    data=client_sock.recv(1024)
    if data=="left":
        print 'left'
        bot.servoRun(7,2,20)
    if data=="right":
        print 'right'
        bot.servoRun(7,2,160)
    if data=="duojistop":
        print 'duojistop'
        bot.servoRun(7,2,90)
    print data

client_sock.close()
server_sock.close()
print "all done"
       
