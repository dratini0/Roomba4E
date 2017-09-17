#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from VisionAnalysis import image_analysis
from libroomba import Roomba

LOOKING_FOR = "water_bottle"

def founditem(weightdict):
    result = max(weightdict.items(), key=lambda x: x[1])
    if result[1] > 0.01:
        return result[0]

r = Roomba("/dev/ttyUSB0")
r.send_opcode("CLEAN")

while True:
    result = image_analysis()
    print(result)
    if founditem(result) == LOOKING_FOR:
        break

r.send_opcode("CLEAN")

r.drive_straight(30)

while True:
    sensorResult = r.get_sensors()
    if sensorResult.light_bumper != 0:
        break
    result = image_analysis()
    print(result)
    if founditem(result) != LOOKING_FOR:
        break

r.stop_drive()

