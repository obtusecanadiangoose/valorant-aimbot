import socket
import os

localIP     = "192.168.1.191"

localPort   = 20001

bufferSize  = 1024

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]
    
    msg = str(message)
    command = "echo "+msg[2:-1]+" --b1 | ~/hid_gadget_test /dev/hidg0 mouse"
    os.system(command)
