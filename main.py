#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from VisionAnalysis import image_analysis
from libroomba import Roomba
from sys import exit

LOOKING_FOR = "water_bottle"
THRESHOLD = .3

def founditem(weightdict):
    return weightdict[LOOKING_FOR] > THRESHOLD

r = Roomba("/dev/ttyUSB0")
r.send_opcode("SAFE")
r.send_opcode("CLEAN")

while True:
    result = image_analysis()
    print(result)
    if founditem(result):
        break

r.send_opcode("CLEAN")

for i in range(6):
    result = image_analysis()
    print(result)
    if founditem(result):
        break
    r.turn_ccw_amount(60)
else:
    print("Not found after rotation")
    exit()

r.drive_straight(30)

while True:
    sensorResult = r.get_sensors()
    if sensorResult.light_bumper != 0:
        break
    result = image_analysis()
    print(result)
    if not founditem(result):
        break

r.stop_drive()
