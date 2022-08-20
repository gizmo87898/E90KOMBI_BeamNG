from E65CAN_VirtualCAS import VirtualCAS
from E90CAN_Counters import Counters
from periodicrun import PeriodicSleeper
from can.interface import Bus
import can
import time
can.rc['interface'] = 'seeedstudio'
can.rc['channel'] = 'COM8'
can.rc['bitrate'] = 100000
virtualCAS = VirtualCAS()
bus = Bus()
counters = Counters()
def __init__(self):
    counters = Counters(bus)
    
def main():
    print("Hello World")
    
if __name__ == "__main__":
    main()

def loop200ms():
        bus.send(can.Message(data = [0x45,0x40,0x21,0x8F,0xFE], arbitration_id = 0x130, is_extended_id=False))
        counters.sendABS(bus)

sleeper200ms = PeriodicSleeper(loop200ms, 0.2)
 
