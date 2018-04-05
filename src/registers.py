from enum import IntEnum

class Registers(IntEnum):
    PHASE1_TEMPERATURE  = 288, # 0120h
    PHASE1_KW           = 290, # 0124h
    PHASE1_KVA          = 292, # 0126h
    PHASE1_KVAR         = 294, # 0128h