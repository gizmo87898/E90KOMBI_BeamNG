from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class Fuel:
    starttime = time.time()
    fuel = 100 # off, parking, cruise, sport, sport_reverse, reverse, reverse_cruise, reverse_parking, reverse_sport, reverse_sport_reverse, neutral, neutral_reverse, neutral_sport, neutral_sport_reverse, neutral_parking, neutral_parking_reverse, neutral_sport_parking, neutral_sport_parking_reverse, neutral_reverse_parking, neutral_reverse_parking_reverse, neutral_reverse_sport, neutral_reverse_sport_reverse, neutral_reverse_cruise, neutral_reverse_cruise_reverse, neutral_reverse_sport_cruise, neutral_reverse_sport_cruise_reverse, neutral_reverse_sport_cruise_parking, neutral_reverse_sport_cruise_parking_reverse, neutral_reverse_sport_cruise_parking_sport, neutral_reverse_sport_cruise_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_
    def __init__(self):
        print("Fuel Controller initialized")

    def setFuel(self, status):
        self.fuel = status

    def sendFuel(self, bus):
        level = self.fuel / 3
        data = [0,int(level),0,0,0]

        data[2] = data[0]
        data[3] = data[1]
        try:
            bus.send(can.Message(data = data, arbitration_id = 0x349, is_extended_id=False))
        except can.CanError:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Message not sent")

    
# oil pan
# fron diff bolts
# front guibo bolts
# front driveshaft bolts
# oil + filter
# front guibo
