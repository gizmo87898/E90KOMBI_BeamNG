from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
class Counters:
    
    ABScounter = 240
    ABSmessage = can.Message(data = [0xF4,0xFF], arbitration_id = 0x0C0, is_extended_id=False)

    AirbagCounter = 0
    AirbagMessage = can.Message(data = [0x00,0xFF], arbitration_id = 0x0D7, is_extended_id=False)

    def __init__(self):
        print("Counters initialized")


    def sendABS(self, bus):
        if self.ABScounter == 255:
            self.ABScounter = 240
        else:
           self.ABScounter += 1
        data = [self.ABScounter, 0xFF] 
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x0C0, is_extended_id=False))
        except can.CanError:
            print("Message not sent")
        
    
    def sendAirbag(self, bus):
        if self.AirbagCounter == 255:
            self.AirbagCounter = 0
        else:
           self.AirbagCounter += 1
        data = [self.AirbagCounter, 0xFF] 
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x0D7, is_extended_id=False))
        except can.CanError:
            print("Message not sent")


