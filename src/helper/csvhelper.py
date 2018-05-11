import csv
import os.path
from decimal import Decimal
from em340.measurement import Measurement

class CsvHelper(object):
    def readMeasurements(self, filename: str) -> str:
        result = ''
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result += '{}\n'.format(row)
        f.close()
        return result

    def writeMeasurement(self, filename: str, data: Measurement, timer: float) -> None:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([timer, data.p, data.s, data.q,data.u,data.i])
        f.close()
