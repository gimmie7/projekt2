class Measurement(object):
    def __init__(self, timestamp: float, p: float, s: float, d: float, q: float):
        '''
        A measurement with real-, apparent-, distortion- and reactive power\n
        :param float timestamp: The timestamp of the measurement\n
        :param float p: The real power (Wirkleistung)\n
        :param float s: The apparent power (Scheinleistung)\n
        :param float d: The distortion power (Verzerrungsleistung)\n
        :param float q: The reactive power (Blindleistung)
        '''
        self.timestamp = timestamp
        self.p = p
        self.s = s
        self.d = d
        self.q = q
