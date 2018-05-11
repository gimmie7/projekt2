import argparse
import datetime
from em340.em340 import Em340
from em340.measurement import Measurement
from helper.scheduler import PeriodicScheduler
from helper.csvhelper import CsvHelper

# Settings and default values
port = 'COM4' # serial port
interval = 1 # in seconds
filename_out = 'samples.csv'
debug_mode = False
parser = argparse.ArgumentParser()
parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4")
parser.add_argument("--i", help="interval in seconds for reading/writing data", type=float)
parser.add_argument("--o", help="file name to write data to, e.g. bulb-20180417.csv")
parser.add_argument("--d", help="debug mode with additional logging", action='store_true')
args = parser.parse_args()

if args.p:
    port = args.p
if args.i:
    interval = args.i
if args.o:
    filename_out = args.o
if args.d:
    debug_mode = True

# Inizialize Em340
em340 = Em340(port)
csvhelper = CsvHelper()
filename_out = 'data_samples/{}'.format(filename_out)

print('run script with the following settings: port={0}, intervall in sec={1}, out dir={2}, debug mode={3}'
.format(port, interval, filename_out, debug_mode))

timer = 0
def write_measurement():
    '''
    reads data from em340, writes it to csv and prints it to the default out stream
    '''
    global timer
    measurement = em340.read_phase1()
    csvhelper.writeMeasurement(filename_out, measurement,timer)
    outputMsg = ('{0}: P={1}W, S={2}VA, Q={3}VAR,U={4}V,I={5}A'
    .format(timer, measurement.p, measurement.s, measurement.q, measurement.u, measurement.i))
    timer = timer + 1
    print(outputMsg)

# Periodic reading/writing
periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(interval, write_measurement) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  