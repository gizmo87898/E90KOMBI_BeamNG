from urllib.request import parse_keqv_list
from periodicrun import PeriodicSleeper
import can
import time
from threading import Timer
class Lights:
    starttime = time.time()
    lightstatus = "parking" # off, parking, cruise, sport, sport_reverse, reverse, reverse_cruise, reverse_parking, reverse_sport, reverse_sport_reverse, neutral, neutral_reverse, neutral_sport, neutral_sport_reverse, neutral_parking, neutral_parking_reverse, neutral_sport_parking, neutral_sport_parking_reverse, neutral_reverse_parking, neutral_reverse_parking_reverse, neutral_reverse_sport, neutral_reverse_sport_reverse, neutral_reverse_cruise, neutral_reverse_cruise_reverse, neutral_reverse_sport_cruise, neutral_reverse_sport_cruise_reverse, neutral_reverse_sport_cruise_parking, neutral_reverse_sport_cruise_parking_reverse, neutral_reverse_sport_cruise_parking_sport, neutral_reverse_sport_cruise_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_parking_reverse, neutral_reverse_sport_cruise_parking_sport_parking_sport_parking_sport_
    def __init__(self):
        print("Light Controller initialized")

    def setLights(self, status):
        self.lightstatus = status

    def sendLights(self, bus):
        match self.lightstatus:
            case "off":
                data = [0x00,0x00,0xF7]
            case "parking":
                data = [0x05,0x18,0xF7]
            case "headlights":
                data = [0x07,0x18,0xF7]
            case "highbeam":
                data = [0x39,0xF1,0xF7]

        try:
            bus.send(can.Message(data = data, arbitration_id = 0x21A, is_extended_id=False))
        except can.CanError:
            print("Time: " + str(float(time.time() - self.starttime)))
            print("Message not sent")

    
# oil pan
# fron diff bolts
# front guibo bolts
# front driveshaft bolts
# oil + filter
# front guibo
