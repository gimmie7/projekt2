import argparse
import datetime
from em340.em340 import Em340
from em340.measurement import Measurement
from helper.scheduler import PeriodicScheduler
from helper.csvhelper import CsvHelper

# Settings
port = 'COM4' # serial port
interval = 0.5 # in seconds
debug_mode = False
parser = argparse.ArgumentParser()
parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4")
parser.add_argument("--i", help="interval in seconds for reading/writing data", type=float)
parser.add_argument("--d", help="debug mode with additional logging", action='store_true')
args = parser.parse_args()

if args.p:
    port = args.p

if args.i:
    interval = args.i

if args.d:
    debug_mode = True

# Inizialize Em340
em340 = Em340(port)
csvhelper = CsvHelper()

print('run script with the following settings: port={0}, intervall in sec={1}, debug mode={2}'
.format(port, interval, debug_mode))

def write_measurement():
    """reads data from em340 and writes it to csv"""
    measurement = em340.read_phase1()
    csvhelper.writeMeasurement("data_samples/samples.csv", measurement)
    outputMsg = ('{0}: P={1}W, S={2}VA, D={3}VAR, Q={4}VAR'
    .format(datetime.datetime.fromtimestamp(measurement.timestamp).strftime('%Y-%m-%d %H:%M:%S'), 
    measurement.p, measurement.s, measurement.d, measurement.q))
    print(outputMsg)

# Periodic reading/writing
periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(interval, write_measurement) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  