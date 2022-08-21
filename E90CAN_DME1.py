from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
class DME:

    rpm = 845
    throttle = 0 # 255 to 65064
    rpmbyte = 0x0D34
    def __init__(self):
        print("DME initialized")

    def setRPM(self, rpm):
        self.rpm = rpm
        self.rpmbyte = hex(int(self.rpm) * 4)

    def setThrottle(self, throttle):
        self.throttle = throttle

    def sendDME(self, bus):
        self.rpmbyte = hex(int(self.rpm) * 4)
        data = [
            0x5F,
            0x59,
            0xFF, # Throttle
            0x00, # Throttle
            int(self.rpmbyte[2:3], 16),  # RPM
            int(str('0' + self.rpmbyte[4]), 16), # RPM
            0x80, 
            0x99
            ]
        print("RPM: " + str(self.rpm))
        print("RPM Byte: " + self.rpmbyte)
        bus.send(can.Message(data = data, arbitration_id = 0x0AA, is_extended_id=False))
    
   
