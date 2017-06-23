#!/usr/bin/env python
from config import *
from crc16 import *
from time import sleep
import socket
import sys

FLAG = {'IS_RUNNING': False, 'DETECT_OBJ': False}

def _packet(packet):
    return packet.encode()

class gripper():
    def __init__(self, host):
        #### Server Socket info. #####
        self.HOST = host
        self.PORT = 603
        self.BUFSIZE = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.gripperSocket = ''

        # Default Speed & Force
        self.speed = 255
        self.force = 255

        self.FLAG = FLAG
        self.IS_RUNNING = False
        self.DETECT_OBJ = False
        self.RESET = False

        # Connect to gripper
        self._connect()
        self._Reset()

    def _connect(self):
        try:
            self.gripperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.gripperSocket.connect(self.ADDR)
        except:
            print("Please check the connect for gripper", file=sys.stderr)
            sys.exit()

    def _mv_cmd_gen(self, pose, speed, force):
        data = BASIC_MOVE_COMMAND + format(pose, '02x') + format(speed, '02x') + format(force, '02x')
        return GetCrc16(data).encode()

    def _Reset(self):
        while True :
            self.gripperSocket.send(_packet(RESET_INIT_ACT))
            sleep(0.1)
            CHK = self.gripperSocket.recv(self.BUFSIZE)
            if CHK == RESET_KEY:
                break

        self.gripperSocket.send(_packet(SET_INIT_ACT))
        sleep(0.1)

        while True:
            self.gripperSocket.send(_packet(WAIT_INIT_ACT))
            data_raw = self.gripperSocket.recv(self.BUFSIZE)

            if data_raw == INIT_ACT_COMPLETE:
                break

        self.RESET = True

    def move(self, pose):
        cmd = self._mv_cmd_gen(pose, self.speed , self.force)  # Packet generator
        self.gripperSocket.send(cmd)  # move gripper

        while True:
            self.IS_RUNNING, self.DETECT_OBJ = self.chk_status(pose)
            if self.IS_RUNNING == False :
                break
            if self.DETECT_OBJ == True :
                break

    def chk_status(self,pose):
        self.gripperSocket.send(_packet(WAIT_MOVE))
        data_raw = self.gripperSocket.recv(self.BUFSIZE)  # data read
        sleep(0.1)
        data = data_raw.decode()

        # Data Encoding
        if len(data) == 22:
            data_pack = [data[6:8], data[14:16]]

            self.status = "{0:08b}".format(int(data_pack[0], 16))

            cur_pose = data_pack[1]
            pose = '{:02x}'.format(pose)

            gOBJ = self.status[0:2]

            if gOBJ == '00' or gOBJ == '11':
                #print("No object detect")
                self.DETECT_OBJ = False
            elif gOBJ == '10':
                #print("object detect")
                self.DETECT_OBJ = True

            if pose == cur_pose:
                #print('Stopped')
                self.IS_RUNNING = False

            else:
                #print('running')
                self.IS_RUNNING = True

            return self.IS_RUNNING, self.DETECT_OBJ
        return None, None

    def set_gripper(self, speed, force):
        self.speed = speed
        self.force = force

    def close(self):
        # Close Action
        self.move(pose=226)

    def open(self):
        # Open Action
        self.move(pose=13)

    def shutdown(self):
        pass