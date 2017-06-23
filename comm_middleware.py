# Complete version, Lan to Serial or Serial to Lan, Communication middleware

import socket
import serial 
import time
import binascii
from thread import *

"""
= Requirement  
Python 2.7

= Description
Robotiq 2-Finger Gripper Server IP : Equal to Robot IP, PORT : 603 
After received control command from PC(Socket), command transfer to Serial. 

= Usage
This program is ur3 Background execution Program, must move file to ur3.
First Log in ur, id : 'root', pwd : 'easybot'
and downloads pyserial.tar file, Install to ur3 using usb. (in ur3 console)
Write 'python comm_middleware.py &' to OS path(/etc/init.d)

Notice : Removed provided Robotiq Gripper urcap.
"""

###### Robot, Server girpper control
HOST = ''
PORT = 603
BUFSIZE = 1024
ADDR = (HOST,PORT)

# Open socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect Device : Gripper info
Gripper_COM = "/dev/ttyUSB0"
baud = 115200
ser = serial.Serial(Gripper_COM, baud, timeout=0)

# Bind to a address and port
serverSocket.bind(ADDR) 
serverSocket.listen(10)

def clientthread(conn):
  while True :
    data = conn.recv(BUFSIZE) # from PC
    # print("Recive Command : ",data) # print received data

    data = data.decode("hex")
    ser.write(data)
    data_raw = ser.readline()
    data = binascii.hexlify(data_raw)

    # print data # print transmiited data
    
    conn.send(data) # to PC
      
    if not data :
      break

  conn.close()
 
while True:
  #wait to accept a connection - blocking call
  conn, addr = serverSocket.accept()
  start_new_thread(clientthread, (conn,))

s.close()
ser.close()
