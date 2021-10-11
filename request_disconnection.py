##################################################
## stript to create radio link disconnection
##################################################
## Author: Paulo Rettore and Robeto Rigolin
## Status: close
## Date: 2019
##################################################
import argparse
import socket
import struct

# Send the disconnection time to the Raspberry pi controlling the relay
def sendDisruptionTime(ipAddress, servicePort, disconnectionTime):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ipAddress, servicePort))

    s.sendall(struct.pack('f', disconnectionTime))

    data = s.recv(1024)
    print('Received', repr(data))


if __name__ == '__main__':

    print('Started link disconnection over military radios')

    parser = argparse.ArgumentParser(description="Link disconnection over military radios!")
    parser.add_argument("-i", "--ip", help="RaspberryPi IP", type=str, required=True, default='192.168.1.141')
    parser.add_argument("-p", "--port", help="RaspberryPi Port", type=str, required=True, default='2002')
    parser.add_argument("-t", "--time", help="Disconnection time", type=float, required=True)
    args = parser.parse_args()

    if args.time and args.ip and args.port:
        # disconnect the coaxial link
        sendDisruptionTime(args.time, args.port, args.time)
    else:
        print("Exiting the link disconnection! There are no enough arguments")