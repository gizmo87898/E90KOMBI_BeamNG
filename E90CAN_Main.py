from E65CAN_VirtualCAS import VirtualCAS
from E90CAN_Counters import Counters
from E90CAN_Speed import Speed
from E90CAN_Handbrake import Handbrake
from E90CAN_DME1 import DME
from E90CAN_IndicatorController import Indicators
from E90CAN_Lights import Lights
from E90CAN_SendStack import SendStack
from E90CAN_GearIndicator import GearIndicator
from E90CAN_Fuel import Fuel
from E90CAN_GUI import GUI
from E90CAN_Outgauge import OutGauge
from periodicrun import PeriodicSleeper
from can.interface import Bus
import can
import time
import socket
import struct
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
can.rc['interface'] = 'seeedstudio'
can.rc['channel'] = 'COM8'
can.rc['bitrate'] = 100000

virtualCAS = VirtualCAS()

canbus = Bus()
bus = SendStack(canbus)
DSCspeed = Speed()
counters = Counters()
handbrake = Handbrake()
dme = DME()
indicators = Indicators()
lights = Lights()
outgauge = OutGauge()
starttime = time.time()
gearindicator = GearIndicator()
fuel = Fuel()
app = QtWidgets.QApplication(sys.argv)
gui = GUI()
stack = [can.message]
global counter
counter = 0x0D
def __init__(self):
    counters = Counters(bus)
    
def main():
    print("Hello World") 
    
if __name__ == "__main__":
    main()

def dmeFunc():
    dme.sendDME(bus)
sleeper100ms = PeriodicSleeper(dmeFunc, 0.05)

def casFunc():
    virtualCAS.sendIgnition(bus)
casSleeper = PeriodicSleeper(casFunc, 0.1)

def absCounterLoop():
    counters.sendABS(bus)
absSleeper = PeriodicSleeper(absCounterLoop, 0.1)

def airbagFunc():
    counters.sendAirbag(bus)
airbagSleeper = PeriodicSleeper(airbagFunc, 0.2)

def handbrakeFunc():
    handbrake.sendHandbrake(bus)
handbrakeSleeper = PeriodicSleeper(handbrakeFunc, 0.2)

def fuelFunc():
    fuel.sendFuel(bus)
fuelSleeper = PeriodicSleeper(fuelFunc, 0.2)


def lightsFunc():
    lights.sendLights(bus)
lightsSleeper = PeriodicSleeper(lightsFunc, 0.2)


def gearFunc():
    gearindicator.sendGear(bus)
gearSleeper = PeriodicSleeper(gearFunc, 0.2)


def indicatorsFunc():
    indicators.sendIndicators(bus)
indicatorsSleeper = PeriodicSleeper(indicatorsFunc, 0.2)

def speedCounterLoop():
    DSCspeed.sendSpeed(bus)
speedSleeper = PeriodicSleeper(speedCounterLoop, 0.2)


def loop5000ms():
    data = [
        time.localtime().tm_hour, # Hour
        time.localtime().tm_min, # minute
        time.localtime().tm_sec, #second
        time.localtime().tm_mday, #day of month
        int(hex(time.localtime().tm_mon) + "F", 16), #month (1F = Jan, 2F = Feb, 3F = March, 4F = April.....)
        int(hex(time.localtime().tm_year)[3] + hex(time.localtime().tm_year)[4], 16),
        int(hex(time.localtime().tm_year)[2], 16), #year  (7DF HEX = 2015 DEC)
        242 #idk
        ]
    try:
        bus.send(can.Message(data = data, arbitration_id = 0x39E, is_extended_id=False))
    except:
        print("Time: " + str(float(time.time() - starttime)))
        print("Time CAN Message error")

timeLoop = PeriodicSleeper(loop5000ms, 5)
# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to LFS.
sock.bind(('127.0.0.1', 4444))
while True:
    outgauge_pack = outgauge.getPack()
    gametime = outgauge_pack[0]
    car = outgauge_pack[1]
    flags = outgauge_pack[2]
    gear = outgauge_pack[3] # reverse = 0, park/neutral = 1, 1st = 2, etc
    try:
        str(gear)[5]
    except:
        gearindicator.setGear("8")

    else:
        match str(gear)[5]:
            case "0":
                gearindicator.setGear("r")
            case "1":
                gearindicator.setGear("n")
            case "2":
                gearindicator.setGear("1")
            case "3":
                gearindicator.setGear("2")
            case "4":
                gearindicator.setGear("3")
            case "5":
                gearindicator.setGear("4")
            case "6":
                gearindicator.setGear("5")
            case "7":
                gearindicator.setGear("6")
            case "8":
                gearindicator.setGear("7")
            case default:
                print("Unknown gear:" + str(gear)[5])
    speed = outgauge_pack[5]
    DSCspeed.setSpeed(speed*2.23694)
    rpm = outgauge_pack[6]
    turbo = outgauge_pack[7] # bar
    engtemp = outgauge_pack[8] # C
    dme.setCoolant(engtemp)
    dme.setRPM(rpm)
    virtualCAS.setIgnition("run")
    fuellevel = outgauge_pack[9] # 0 to 1
    fuel.setFuel(fuellevel * 100)
    oilpressure = outgauge_pack[10] # bar
    oiltemp = outgauge_pack[11] # C
    dashlights = format(outgauge_pack[12], "016b") # dash lights available (see DL_x)
    showlights = format(outgauge_pack[13], "016b") # Dash lights currently switched on
    #1st bit:
    #2nd bit: 
    #3rd bit: 
    #4th bit:
    #5th bit:
    #6th bit: ABS Active
    #7th bit: Is Engine stalled
    #8th bit:
    #9th bit:

    #10th bit: Right Blinker
    #11th bit: Left Blinker
    #12th bit: DSC Active
    #13th bit:
    #14th bit: E-brake
    #15th bit: High-Beam
    #16th bit:
    throttle = outgauge_pack[14] # 0 to 1
    brake = outgauge_pack[15] # 0 to 1
    clutch = outgauge_pack[16]# 0 to 1
    display1 = outgauge_pack[17]
    display2 = outgauge_pack[18]
    
    # Set the rpm frame
    if showlights[14] == "1":
        print("High-Beam Active")
    
    if showlights[9] == "1":
        if showlights[10] == "1":
            indicators.setIndicators('hazard')
        else:
            indicators.setIndicators('right')
    elif showlights[10] == "1":
        indicators.setIndicators("left")
    else:
        indicators.setIndicators("off")

    if showlights[14] == "1":
        handbrake.setHandbrake("on")
    else:
        handbrake.setHandbrake("off")
    