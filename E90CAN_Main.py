from E65CAN_VirtualCAS import VirtualCAS
from E90CAN_Counters import Counters
from E90CAN_Speed import Speed
from E90CAN_Handbrake import Handbrake
from E90CAN_DME1 import DME
from E90CAN_IndicatorController import Indicators
from periodicrun import PeriodicSleeper
from can.interface import Bus
import can
import time
import socket
import struct
can.rc['interface'] = 'seeedstudio'
can.rc['channel'] = 'COM8'
can.rc['bitrate'] = 100000
virtualCAS = VirtualCAS()
bus = Bus()
DSCspeed = Speed()
counters = Counters()
handbrake = Handbrake()
dme = DME()
indicators = Indicators()
starttime = time.time()
def __init__(self):
    counters = Counters(bus)
    
def main():
    print("Hello World") 
    
if __name__ == "__main__":
    main()

def loop200ms():
    print("====================")
    print("Time: " + str(float(time.time() - starttime)))
    try:
        bus.send(can.Message(data = [0x45,0x40,0x21,0x8F,0xFE], arbitration_id = 0x130, is_extended_id=False))
    except can.CanError:
        print("Ignition not sent")
    counters.sendABS(bus)
    counters.sendAirbag(bus)
    DSCspeed.sendSpeed(bus)
    handbrake.sendHandbrake(bus)
    dme.sendDME(bus)

def loop5000ms():
    print(time.localtime())
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
    print(data)
    try:
        bus.send(can.Message(data = data, arbitration_id = 0x39E, is_extended_id=False))
    except:
        print("Time CAN Message error")
sleeper200ms = PeriodicSleeper(loop200ms, 0.2)
sleeper5000ms = PeriodicSleeper(loop5000ms, 5)

# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to LFS.
sock.bind(('127.0.0.1', 4444))

def update():
    
    data = sock.recv(96)
    if not data:
        return
    outgauge_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
    gametime = outgauge_pack[0]
    car = outgauge_pack[1]
    flags = outgauge_pack[2]
    gear = outgauge_pack[3] # reverse = 0, neutral = 1, 1st = 2, etc
    speed = outgauge_pack[5]
    rpm = outgauge_pack[6]
    turbo = outgauge_pack[7] # bar
    engtemp = outgauge_pack[8] # C
    fuel = outgauge_pack[9] # 0 to 1
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
    dme.setRPM(rpm)
    DSCspeed.setSpeed(speed)
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


    #print("Time: %d" % gametime)
    #print("Car: %s" % car)
    #print("Flags: %d" % flags)
    #print("Gear: " + gear.decode("utf-8"))
    #print("Speed: %d" % speed)
    #print("RPM: %d" % rpm)
    #print("Turbo: %d" % turbo)
    #print("Engine Temp: %d" % engtemp)
    ##print("Fuel: %d" % fuel)
    #print("Oil Pressure: %d" % oilpressure)
    #print("Oil Temp: %d" % oiltemp)
    #print("Dash Lights: %d" % dashlights)
    #print("Show Lights: " + showlights)
    #print("Throttle: %d" % throttle)
    #print("Brake: %d" % brake)
    #print("Clutch: %d" % clutch)
    #print("Display 1: " + display1.decode("utf-8") )
    #print("Display 2: " + display2.decode("utf-8") )


# Release the socket.

sleeper100ms = PeriodicSleeper(update, 0.1)