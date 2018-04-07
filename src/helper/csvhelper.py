import csv
import os.path
from decimal import Decimal
from model.measurement import Measurement

class CsvHelper(object):
    def readMeasurements(self, filename: str) -> str:
        result = ''
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result += '{}\n'.format(row)
        f.close()
        return result

    def writeMeasurement(self, filename: str, data: Measurement) -> None:
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if file_exists == False:
                writer.writerow(['Timestamp', 'P[W]', 'S[VA]', 'D[VAR]', 'Qtrans[VAR]'])
            writer.writerow([data.timestamp, data.p, data.s, data.d, data.q])
        f.close()
