from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
import time
class Speed:
    
    ABScounter = 240
    ABSmessage = can.Message(data = [0x13,0x4D,0x46,0x4D,0x33,0x4D,0xD0,0xFF], arbitration_id = 0x1A6, is_extended_id=False)
    speed = 200
    speedbytes = [0x00, 0x00]
    lastsentat = time.time()
    # (((( [time now] - [time last sent] ) / 50(milliseconds)) * [Speed] ) + last reading) 
    def __init__(self):
        print("Counters initialized")

    def setSpeed(self, speed):
        self.speed = speed

    def sendSpeed(self, bus):
        if self.ABScounter == 255:
            self.ABScounter = 240
        else:
           self.ABScounter += 1

        self.speedbytes[0] = int(((( time.time() - self.lastsentat ) / 50) * self.speed ) + self.speedbytes[0]) 
        self.speedbytes[1] = int(((( time.time() - self.lastsentat ) / 50) * self.speed ) + self.speedbytes[1]) 
        self.lastsentat = time.time()
        data = [self.speedbytes[0], self.speedbytes[1],self.speedbytes[0], self.speedbytes[1],self.speedbytes[0], self.speedbytes[1],self.speedbytes[0], self.speedbytes[1]] 
        print("Speed: " + str(self.speed))
        bus.send(can.Message(data = data, arbitration_id = 0x0C0, is_extended_id=False))
    
