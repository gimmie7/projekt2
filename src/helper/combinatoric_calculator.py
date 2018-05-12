from em340.measurement import Measurement
import numpy as np
import itertools

class CombinatoricCalculator(object):
    def calculate(self,totp:float,tots:float,totq:float,toti:float) -> str:
        devices = np.genfromtxt('data_samples/devices.csv',delimiter=',',dtype=None,usecols=(0,1,2,3,4),encoding='UTF-8')
        #print(devices[0][0])
        device = [] # the nearest combination
        label = ''
        val = 10000000 # the nearest value to total
        test= len(devices)
        for l in range(1, len(devices) + 1):
            for x in itertools.combinations(devices, l):
                p = s = q = i = 0
                print(x)
                for y in x:
                    p = p + y[1]
                    s = s + y[2]
                    q = q + y[3]
                    i = i + y[4]
                print('P={}, S{}, Q={}, I={}'.format(p,s,q,i))

                total_x = abs(totp-p) + abs(tots-s) + abs(totq-q) + abs(toti-i)
                if total_x < val:
                    device = x
                    val = total_x
        for d in device:
            label = label + d[0] +'\n'

        return label