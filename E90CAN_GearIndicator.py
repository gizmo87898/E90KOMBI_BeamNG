from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class GearIndicator:

    starttime = time.time()
    counter = 0x0D
    gear = "p" # off, parking, cruise, sport, sport_reverse, reverse, reverse_cruise, reverse_parking, reverse_sport, reverse_sport_reverse, neutral, neutral_reverse, neutral_sport, neutral_sport_reverse, neutral_parking, neutral_parking_reverse, neutral_sport_parking, neutral_sport_parking_reverse, neutral_reverse_parking, neutral_reverse_parking_reverse, neutral_reverse_sport, neutral_reverse_sport_reverse, neutral_reverse_cruise, neutral_reverse_cruise_reverse, neutral_reverse_sport_cruise, neutral_reverse_sport_cruise_reverse, neutral_reverse_sport_cruise_parking, neutral_reverse_sport_cruise_parking_reverse, neutral_reverse_sport_cruise_parking_sport, neutral_reverse_sport_cruise_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_
    def __init__(self):
        print("Gear Indicator initialized")

    def setGear(self, status):
        self.gear = status

    def sendGear(self, bus):
        
        if self.counter == 0xFD:
            self.counter = 0x0D
        else:
            self.counter += 0x10
        match self.gear:
            case "p":
                data = [0xE1,0x0C,0x8F,self.counter,0xF0,0xFF]
            case "r":
                data = [0xD2,0x0C,0x8F,self.counter,0xF0,0xFF]
            case "n":
                data = [0xB4,0x0C,0x8F,self.counter,0xF0,0xFF]
            case "d":
                data = [0x78,0x0C,0x8B,self.counter,0xF0,0xFF]
            case "1":
                data = [0x78,0x5C,0x8B,self.counter,0xF0,0xFF]
            case "2":
                data = [0x78,0x6C,0x8B,self.counter,0xF0,0xFF]
            case "3":
                data = [0x78,0x7C,0x8B,self.counter,0xF0,0xFF]
            case "4":
                data = [0x78,0x8C,0x8B,self.counter,0xF0,0xFF]
            case "5":
                data = [0x78,0x9C,0x8B,self.counter,0xF0,0xFF]
            case "6":
                data = [0x78,0xAC,0x8B,self.counter,0xF0,0xFF]
            case "7":
                data = [0x78,0xBC,0x8B,self.counter,0xF0,0xFF]
            case "8":
                data = [0x78,0xCC,0x8B,self.counter,0xF0,0xFF]
            case default:
                data = [0xE1,0x0C,0x8F,self.counter,0xF0,0xFF]
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x1D2, is_extended_id=False))
        except can.CanError:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Message not sent")

    
# oil pan
# fron diff bolts
# front guibo bolts
# front driveshaft bolts
# oil + filter
# front guibo
