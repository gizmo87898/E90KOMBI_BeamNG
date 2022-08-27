from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class Indicators:
    starttime = time.time()
    status = "off"

    def __init__(self):
        print("Indicators initialized")

    def setIndicators(self, status):
        self.status = status

    def sendIndicators(self, bus):
        data = [
            0x80,
            0xF0,
            ]
        match self.status:
            case "off":
                data = [0x80,0xF0]
            case "left":
                data = [0x91,0xF1]
            case "right":
                data = [0xA1,0xF1]
            case "hazard":
                data = [0xB1,0xF1]
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x1F6, is_extended_id=False))
        except:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Indicator message not sent")
    
   
