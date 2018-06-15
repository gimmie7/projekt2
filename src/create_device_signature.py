import argparse
import csv
import statistics


# Settings and default values
device_name = 'Toaster'
filename_in = 'samples.csv'
filename_out = 'devices.csv'
parser = argparse.ArgumentParser()
parser.add_argument("--d", help="device name, e.g. bulb")
parser.add_argument("--i", help="file name to read data from, e.g. bulb-20180417.csv")
parser.add_argument("--o", help="file name to write data to, e.g. bulb-20180417.csv")
args = parser.parse_args()

if args.d:
    device_name = args.d
if args.i:
    filename_in = args.i
if args.o:
    filename_out = args.o
# Inizialize Em340

filename_in = 'data_samples/{}'.format(filename_in)
filename_out = 'data_samples/{}'.format(filename_out)

print('run script with the following settings: filename_in={0}, filename_out={1}'.format(filename_in, filename_out))

def writeDevice(device_name: str, filename_in: str, filename_out: str) -> None:
    p = []
    s = []
    q = []
    i = []

    with open(filename_in, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            p.append(float(row[1]))
            s.append(float(row[2]))
            q.append(float(row[3]))
            i.append(float(row[5]))
    f.close()

    median_p = statistics.median(p)
    median_s = statistics.median(s)
    median_q = statistics.median(q)
    median_i = statistics.median(i)
    print('{}, P={}W, S={}VA, Q={}var, I={}A'.format(device_name, median_p, median_s, median_q, median_i))

    with open(filename_out, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([device_name, median_p, median_s, median_q, median_i])
    f.close()

writeDevice(device_name, filename_in, filename_out)