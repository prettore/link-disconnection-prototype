##################################################
## Implements a server waiting for a time window
# for the disruption. Given a time window (float)
# the server turn on (HIGH) one pin at the
# Raspberry pi, waits for the given time and
# turn off the pin
##################################################
## Author: Robeto Rigolin and Paulo Rettore
## Status: close
## Date: 2019
##################################################
import argparse
import struct
import time
import socket
import RPi.GPIO as GPIO




def disruptionServer(HOST, PORT):

    print("Disconnection STARTED ", HOST)

    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        count = 0

        # Infinite loop waiting for connections
        while True:
            count = count + 1
            print(' ')
            print('[', count, '] Waiting for a time window...')
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    disruption_time = float(struct.unpack('f', data)[0])
                    print('Received time: ', disruption_time)
                    if not data:
                        break
                    # Get the start time
                    startTime = time.time()
                    print('Start disruption: ', startTime)

                    # Switch on the relay
                    GPIO.output(23, GPIO.HIGH)
                    # Keep it on for a given time
                    time.sleep(disruption_time)
                    # Switch off the relay
                    GPIO.output(23, GPIO.LOW)
                    # Get the end time
                    endTime = time.time()
                    print('End disruption: ', endTime)

                    # Compute the total time in seconds
                    totalTime = endTime - startTime
                    print('Total time: ', totalTime)

                    # Send the message back to the caller
                    conn.sendall(data)

                # TODO implement a proper try/catch conditional structure

    print("Disconnection ENDED !!!")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Link disconnection over military radios!")
    parser.add_argument("-i", "--ip", help="RaspberryPi IP", type=str, required=True, default='192.168.1.141')# Standard loopback interface address (localhost)
    parser.add_argument("-p", "--port", help="RaspberryPi Port", type=str, required=True, default='2002')# Port to listen on (non-privileged ports are > 1023)
    args = parser.parse_args()

    if args.ip and args.port:
        # disconnect the coaxial link
        disruptionServer(args.ip,args.port)
    else:
        print("Exiting the link disconnection server! There are no enough arguments")
