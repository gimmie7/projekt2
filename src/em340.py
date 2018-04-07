#!/usr/bin/env python
import minimalmodbus
import serial
import argparse
from datetime import datetime
from model.measurement import Measurement
from model.registers import Registers as REG
from helper.csvhelper import CsvHelper
from helper.scheduler import PeriodicScheduler

# Settings
PORT = 'COM4'    
MODE = minimalmodbus.MODE_RTU
DEBUG_MODE = False
READ_INTERVAL = 0.5 # in seconds
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# Starting options
parser = argparse.ArgumentParser()
parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4")
parser.add_argument("--d", help="debug mode with additional logging", action='store_true')
args = parser.parse_args()

if args.p:
    PORT = args.p

if args.d:
    DEBUG_MODE = True

print('run script with the following settings: port={0}, mode={1}, debug mode={2}, intervall in sec={3}'
.format(PORT, MODE, DEBUG_MODE, READ_INTERVAL))

# Setup EM340
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

# Data sampling
csvhelper = CsvHelper()

def record_sample():  
    """Read values from em340"""
    try:
        dt = datetime.now()
        p = em340.read_register(REG.PHASE1_KW, 0)
        s = em340.read_register(REG.PHASE1_KVA, 0)
        d = em340.read_register(REG.PHASE1_KVAR, 0)
        q = 0 # TODO: get the correct value
        outputMsg = ('{0}: P={1}W, S={2}VA, D={3}VAR, Q={4}VAR'.format(dt, p, s, d, q))
        measurement = Measurement(dt.timestamp(), p, s, d, q)
        csvhelper.writeMeasurement("data_samples/samples.csv", measurement)
        
        print(outputMsg)
    except ValueError as err:
        print("Failed to read from instrument em340")
        print(err)

# Periodic reading
INTERVAL = READ_INTERVAL
periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(INTERVAL, record_sample) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  
