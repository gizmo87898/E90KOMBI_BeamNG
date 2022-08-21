from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
class Handbrake:
    status = 'off'
    def __init__(self):
        print("Handbrake initialized")

    def setHandbrake(self, handbrake):
        self.status = handbrake
    def sendHandbrake(self, bus):
        if self.status == 'off':
            data = [0xFD,0xFF]
        else:
            data = [0xFE,0xFF]
        print("Handbrake: " + self.status)
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x34F, is_extended_id=False))
        except:
            print("Handbrake message not sent")
    
   
