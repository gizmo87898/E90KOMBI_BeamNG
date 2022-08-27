from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
import time
import math
class Speed:
    speed = 20
    lastspeedvalue = 0
    startedat = time.time()
    data = [0x13,0x4D,0x46,0x4D,0x33,0x4D,0xD0,0xFF] 
    # (((( [time now] - [time last sent] ) / 50(milliseconds)) * [Speed] ) + last reading) 
    def __init__(self):
        print("DSC Speed initialized")

    def setSpeed(self, speed):
        self.speed = int(speed)
        

    def sendSpeed(self, bus):
        
        speed_value = int(self.speed) + int(self.lastspeedvalue)

        #counter = (self.data[6] | (self.data[7] << 8)) & 0x0FFF
        counter = int(1 * math.pi)
        self.lastsentat = time.time()

        
        self.data[0] = min(speed_value, 255)
        self.data[1] = (speed_value >> 8)

        self.data[2] = self.data[0]
        self.data[3] = self.data[1]

        self.data[4] = self.data[0]
        self.data[5] = self.data[1]

        self.data[6] = counter
        self.data[7] = (counter >> 8) | 0xF0

        print(self.data)

        bus.send(can.Message(data = self.data, arbitration_id = 0x1A6, is_extended_id=False))
        self.lastspeedvalue = self.speed
