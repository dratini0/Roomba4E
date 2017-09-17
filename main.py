#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from VisionAnalysis import image_analysis
from libroomba import Roomba

r = Roomba("/dev/ttyUSB0")
r.send_opcode("CLEAN")

while True:
    result = image_analysis()
    if max(result.items(), key=lambda x: x[1])[0].lower() == "water bottle":
        break

r.send_opcode("CLEAN")

r.drive_straight(30)

while True:
    sensorResult = r.get_sensors()
    if sensorResult.light_bumper != 0:
        break
    result = image_analysis()
    if max(result.items(), key=lambda x: x[1])[0].lower() == "water bottle":
        break

r.stop_drive()

