#!/usr/bin/env python
import minimalmodbus
import serial
import argparse
from datetime import datetime
from em340.measurement import Measurement
from em340.registers import Registers as REG
from helper.csvhelper import CsvHelper
from helper.scheduler import PeriodicScheduler

class Em340(object):                                                  
    def __init__(self, port: str):                                                           
        mode = minimalmodbus.MODE_RTU
        minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
        em340 = minimalmodbus.Instrument(port, 1, mode=mode) # port name, slave address (in decimal)
        em340.serial.port          # this is the serial port name
        em340.serial.baudrate = 9600   # Baud
        em340.serial.bytesize = 8
        em340.serial.parity   = serial.PARITY_NONE
        em340.serial.stopbits = 1
        em340.serial.timeout  = 0.05   # seconds
        em340.mode = mode   # rtu or ascii mode
        self.em340 = em340

    def read_phase1(self) -> Measurement:
        """Read values from em340 phase 1"""
        measurement = self.read_phase(1, REG.PHASE1_KW, REG.PHASE1_KVA, REG.PHASE1_KVAR, 0)
        return measurement

    def read_phase(self, phase: int, reg_p: int, reg_s: int, reg_d: int, reg_q: int) -> Measurement:
        """Read values from em340"""
        try:
            timestamp = datetime.now().timestamp()
            p = self.em340.read_register(reg_p, 0)
            s = self.em340.read_register(reg_s, 0)
            d = self.em340.read_register(reg_d, 0)
            q = 0 # TODO: get the correct value
            return Measurement(timestamp, p, s, d, q)
        except ValueError as error:
            print("Failed to read from instrument em340")
            print(error)
