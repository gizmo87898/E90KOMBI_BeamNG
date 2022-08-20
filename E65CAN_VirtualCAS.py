from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
from threading import Timer
class VirtualCAS:
    
    ignition_status = "run"
    counter = 0x0D
    message = can.Message(data = [0x45,0x43,0x39,0xBF,0xCE], arbitration_id = 0x1D2, is_extended_id=False)
    active = "False"
    def __init__(self):
        # self.counter = "0x0D"
        print("GearShifter initialized")

    def setIgnition(self, status):
        self.ignition_status = status

    def sendIgnition(self, bus):

        if self.counter == 0xFD:
            self.counter = 0x0D
            next
        else:
           self.counter += 0x10
        match self.ignition_status:
            case "lock":
                data = [0x00,0xEF,0x34,0x3F,self.counter]
            case "off":
                data = [0x80,0xEF,0x34,0x3F,self.counter]
            case "acc":
                data = [0x41,0x43,0x35,0x3F,self.counter]
            case "run":
                data = [0x45,0x43,0x39,0xBF,self.counter]
            case "start":
                data = [0x45,0x43,0x35,0xBF,self.counter]
        # print(data)
        bus.send(can.Message(data = data, arbitration_id = 0x130, is_extended_id=False))
