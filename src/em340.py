#!/usr/bin/env python
import minimalmodbus
import serial
from datetime import datetime
from scheduler import PeriodicScheduler
from registers import Registers as REG

#Settings
PORT = 'COM4'
MODE = minimalmodbus.MODE_RTU
DEBUG_MODE = False
READ_INTERVAL = 2 # in seconds
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

#Adapt this device to your OS and actual device path
em340 = minimalmodbus.Instrument(PORT, 1, mode=MODE) # port name, slave address (in decimal)

em340.serial.port          # this is the serial port name
em340.serial.baudrate = 9600   # Baud
em340.serial.bytesize = 8
em340.serial.parity   = serial.PARITY_NONE
em340.serial.stopbits = 1
em340.serial.timeout  = 0.05   # seconds
em340.mode = MODE   # rtu or ascii mode

if DEBUG_MODE:
    em340.debug = True

def read_values():  
    """Read values from em340"""
    try:
        temperature = em340.read_register(REG.PHASE1_TEMPERATURE, 2) # Registernumber, number of decimals
        kw = em340.read_register(REG.PHASE1_KW, 2)
        kva = em340.read_register(REG.PHASE1_KVA, 2)
        kvar = em340.read_register(REG.PHASE1_KVAR, 2)
        outputMsg = ('{0}: temperature={1}, kW={2}, kVA={3}, kvar={4}'.format(datetime.now(), temperature, kw, kva, kvar))
        print(outputMsg)
    except ValueError as err:
        print("Failed to read from instrument em340")
        print(err)

def write_values():
    """write values to em340"""
    ## Write a config to the EM340
    #SOME_VALUE = 95
    #em340.write_register(24, SOME_VALUE, 1) # Registernumber, value, number of decimals for storage
    return 0

INTERVAL = READ_INTERVAL
periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(INTERVAL, read_values) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  
