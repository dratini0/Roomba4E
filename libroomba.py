#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from serial import Serial
from struct import Struct
import time

class Roomba(object):

    DEFAULT_BAUD = 115200

    OPCODES = {
        "START": 128,
        "RESET": 7,
        "STOP": 173,
        "BAUD": 129,
        "SAFE": 131,
        "FULL": 132,
        #Cleaning commands
        #scheduling commands
        "DRIVE": 137,
        "DRIVE_DIRECT": 145,
        "DRIVE_PWM": 146,
        "MOTORS": 138,
        "PWM_MOTORS": 144,
        "LEDS": 139,
        "SCHEDULING_LEDS": 162,
        # more actuator commands
        "SENSORS": 142,
    }

    DRIVE_STRUCT = Struct(">hh")
    SENSOR_STRUCT = Struct(">BBBBBBBBBBBBhhBHhbHHHHHHBHBBBBBhhhhhhBHHHHHHBBhhhhhB")

    def __init__(self, portname="/dev/ttyUSB0"):
        self.serial = Serial(portname, self.DEFAULT_BAUD, timeout=1)
        self.send_opcode("START")
        
    def send_byte(self, byte):
        self.serial.write(bytes([byte]))

    def send_opcode(self, opcode):
        self.send_byte(self.OPCODES[opcode])
        print("Sent op {}".format(opcode))

    def drive(self, velocity, radius):
        self.send_opcode("DRIVE")
        self.serial.write(self.DRIVE_STRUCT.pack(velocity, radius))

    def drive_straight(self, velocity):
        self.drive(velocity, 0x7fff)

    def stop_drive(self):
        self.drive(0, 0)

    def get_sensors(self):
        self.send_opcode("SENSORS")
        self.send_byte(100)
        data = self.serial.read(self.SENSOR_STRUCT.size)
        if len(data) < self.SENSOR_STRUCT.size:
            raise Exception("Only read {} bytes instead of {}".format(len(data), self.SENSOR_STRUCT.size))
        rawStruct = self.SENSOR_STRUCT.unpack(data)
        return (0,)*7 + rawStruct

if __name__ == "__main__":
    r = Roomba()
    print(r.SENSOR_STRUCT.size)
    assert r.SENSOR_STRUCT.size == 80
    r.send_opcode("SAFE")
    r.drive_straight(100)
    time.sleep(1)
    r.stop_drive()
    print(r.get_sensors())
