from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class DME:
    starttime = time.time()
    rpm = 3000
    throttle = 0 # 255 to 65064
    rpmbyte = "2EE0"
    coolantTemp = 50
    def __init__(self):
        print("DME initialized")

    def setRPM(self, rpm):
        self.rpm = rpm
        self.rpmbyte = str(hex(int(self.rpm) * 4))
        if self.rpmbyte.__len__() == 5:
            self.rpmbyte = "0" + self.rpmbyte[2:5]
        elif self.rpmbyte.__len__() == 6:
            self.rpmbyte = self.rpmbyte[2:6]
    def setThrottle(self, throttle):
        self.throttle = throttle

    def setCoolant(self, temp):
        self.coolantTemp = temp

    def sendDME(self, bus):
        if self.rpmbyte.__contains__("x"):
            self.rpmbyte = "0000"
        data = [
            0x5F,
            0x59,
            0xFF, # Throttle
            0x00, # Throttle
            int(self.rpmbyte[2:4], 16),  # RPM
            int(self.rpmbyte[0:2], 16), # RPM
            0x80, 
            0x99
            ]
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x0AA, is_extended_id=False))
        except can.CanError:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Message not sent")

        try:
            bus.send(can.Message(data = [int(self.coolantTemp)+48, 0xFF,0x63,0xCD,0x5D,0x37,0xCD,0xA8], arbitration_id = 0x1D0, is_extended_id=False))
        except can.CanError:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Message not sent")

    
# oil pan
# fron diff bolts
# front guibo bolts
# front driveshaft bolts
# oil + filter
# front guibo
