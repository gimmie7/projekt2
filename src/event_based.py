import argparse
import datetime
import numpy
from em340.em340 import Em340
from em340.measurement import Measurement
from helper.scheduler import PeriodicScheduler
from helper.csvhelper import CsvHelper

# Settings and default values
port = 'COM4' # serial port
parser = argparse.ArgumentParser()
parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4")
args = parser.parse_args()

if args.p:
    port = args.p

# Inizialize Em340
em340 = Em340(port)

print('run script with the following settings: port={0}'.format(port))

active_devices = []
active_power_total = 0
devices = numpy.genfromtxt('data_samples/devices.csv',delimiter=',',dtype=None,usecols=(0,1,2,3,4),encoding='UTF-8')

def guess(measurement: Measurement):
    global active_devices, active_power_total, devices

    difference = 1000000
    guessed_device = None
    for device in devices:
        difference_temp = 0
        if active_power_total < measurement.p: # device added
            difference_temp = abs(active_power_total + device[1] - measurement.p)
        else: # device removed
            difference_temp = abs(active_power_total - device[1] - measurement.p)
            
        if difference_temp < 25 and difference_temp < difference:
            guessed_device = device[0]
            difference = difference_temp

    if guessed_device != None:
        if measurement.p > active_power_total:
            if guessed_device not in active_devices:
                active_devices.append(guessed_device)
        else:
            if guessed_device in active_devices:
                active_devices.remove(guessed_device)

        active_power_total = measurement.p

    return guessed_device

def read():
    global active_power_total, active_devices

    measurement = em340.read_phase1()
    print(str(measurement.p) + ' ' + str(measurement.s))
    
    if abs(active_power_total - measurement.p) > 25:
        guessed_device = guess(measurement)
        if guessed_device != None:
            print(active_devices)

# Periodic reading/writing
periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(5, read) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  