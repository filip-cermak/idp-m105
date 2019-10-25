# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:50:31 2019

@author: Filip
"""

import socket
import time

def send_message_safe(MESSAGE):
    # =============================================================================
    # dependencies: socket, time
    # Sends input string to the arduino, has hardcoded IP and port address,
    # if ACK is not received, return -1
    # if ACK is received but FINISHED not, return 0
    # if ACK and FINISHED received, return 1
    #
    # ACK as not received if waiting > 1 sec from sending the message
    # as not received if waiting > 1 sec from sending the message
    # =============================================================================

    UDP_IP = "192.168.137.49" #changes everytime new connection is established
    UDP_PORT = 2390

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    time_message_sent = time.time()

    ACK = ''

    while ACK== '':
        ACK, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if(time.time() - time_message_sent > 1):
            return -1

    FINISHED = ''

    print('here')

    while FINISHED== '':
        FINISHED, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print('there')
        if(time.time() - time_message_sent > 2):
            return 0

    return 1

def send_message_unsafe(MESSAGE):
    # =============================================================================
    # dependencies: socket
    # Sends input string to the arduino, has hardcoded IP and port address,
    # wait until FINISHED flagged received
    #
    # if ACK not received, Python script stuck in endless loop
    # =============================================================================

    UDP_IP = "192.168.137.49" #changes everytime new connection is established
    UDP_PORT = 2390

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

    ACK = ''

    while ACK== '':
        ACK, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
