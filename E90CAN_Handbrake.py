from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class Handbrake:
    status = 'off'
    starttime = time.time()
    def __init__(self):
        print("Handbrake initialized")

    def setHandbrake(self, handbrake):
        self.status = handbrake
    def sendHandbrake(self, bus):
        if self.status == 'off':
            data = [0xFD,0xFF]
        else:
            data = [0xFE,0xFF]
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x34F, is_extended_id=False))
        except:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Handbrake message not sent")
    
   
