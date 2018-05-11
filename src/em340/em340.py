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
        '''
        Read values from em340 phase 1\n
        :return: the Measurement
        '''
        measurement = self.read_phase(1, REG.L1_WIRKLEISTUNG_P, REG.L1_SCHEINLEISTUNG_S, REG.L1_BLINDLEISTUNG_Q,REG.L1_SPANNUNG_U,REG.L1_STROM_I)
        return measurement

    # todo: do we need the distortion power or is it a calculated value?
    def read_phase(self, phase: int, reg_p: int, reg_s: int, reg_q: int,reg_u: int,reg_i: int) -> Measurement:
        '''
        Read values from em340\n
        :param int phase: The phase to read from. Possible values are 1, 2, 3\n
        :param int reg_p: The register to read the real power (Wirkleistung)\n
        :param int reg_s: The register to read the apparent power (Scheinleistung)\n
        :param int reg_d: The register to read the distortion power (Verzerrungsleistung)\n
        :param int reg_q: The register to read the reactive power (Blindleistung)\n
        :return: the Measurement
        '''
        try:
            timestamp = datetime.now().timestamp()
            p = self.em340.read_register(reg_p, 1)
            s = self.em340.read_register(reg_s, 1)
            q = self.em340.read_register(reg_q, 1)
            u = self.em340.read_register(reg_u, 1)
            i = self.em340.read_register(reg_i, 3)
            return Measurement(timestamp, p, s, q,u,i)
        except ValueError as error:
            print("Failed to read from instrument em340")
            print(error)
