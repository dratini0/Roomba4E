#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from serial import Serial
from struct import Struct
import time
from collections import namedtuple

SensorData = namedtuple("SensorData", [
    "unused0",
    "unused1",
    "unused2",
    "unused3",
    "unused4",
    "unused5",
    "unused6",
    "bumps_wheel_drops",
    "wall",
    "cliff_left",
    "cliff_front_left",
    "cliff_front_right",
    "cliff_right",
    "virtual_wall",
    "wheel_overcurrents",
    "dirt_detect",
    "unused16",
    "infrared_char_omni",
    "buttons",
    "distance",
    "angle",
    "charging_state",
    "voltage",
    "current",
    "temperature",
    "battery_charge",
    "battery_capacity",
    "wall_signal",
    "cliff_left_signal",
    "cliff_front_left_signal",
    "cliff_front_right_signal",
    "ciff_right_signal",
    "unused32",
    "unused33",
    "charging_sources_available",
    "oi_mode",
    "song_number",
    "song_playing",
    "number_of_stream_packets",
    "requested_velocity",
    "requested_radius",
    "requested_right_velocity",
    "requested_left_velocity",
    "left_encoder_counts",
    "right_encoder_counts",
    "light_bumper",
    "light_bump_left_signal",
    "light_bump_front_left_signal",
    "light_bump_front_center_left_signal",
    "light_bump_front_center_right_signal",
    "light_bump_front_right_signal",
    "light_bump_right_signal",
    "infrared_char_left",
    "infrared_char_right",
    "left_motor_current",
    "right_motor_current",
    "main_brush_motor_currnet",
    "side_brush_motor_current",
    "stasis",
])

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
        "CLEAN": 135,
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
    SENSOR_STRUCT = Struct(">BBBBBBBBBBBBhhBHhbHHHHHHBHBBBBBhhhhhhhBHHHHHHBBhhhhB")

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

    def spin_cw(self, velocity):
        self.drive(velocity, -1)

    def spin_ccw(self, velocity):
        self.drive(velocity, 1)

    def get_sensors(self):
        self.send_opcode("SENSORS")
        self.send_byte(100)
        data = self.serial.read(self.SENSOR_STRUCT.size)
        if len(data) < self.SENSOR_STRUCT.size:
            raise Exception("Only read {} bytes instead of {}".format(len(data), self.SENSOR_STRUCT.size))
        rawStruct = self.SENSOR_STRUCT.unpack(data)
        preparedStruct = (0,)*7 + rawStruct
        return SensorData(*preparedStruct)

    def turn_ccw_amount(self, angle, velocity=100):
        self.get_sensors()
        self.spin_ccw(velocity)
        totalturn = 0
        while totalturn < angle:
            totalturn += self.get_sensors().angle
        self.stop_drive()

if __name__ == "__main__":
    r = Roomba()
    assert r.SENSOR_STRUCT.size == 80
    r.send_opcode("SAFE")
    #r.drive_straight(-100)
    #time.sleep(1)
    #r.drive_straight(100)
    #time.sleep(1)
    #r.stop_drive()
    r.turn_ccw_amount(60)
    while True:
        print(r.get_sensors())
        time.sleep(1)
