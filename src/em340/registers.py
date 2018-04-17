from enum import IntEnum

class Registers(IntEnum):
    # Phase 1
    L1_WIRKLEISTUNG_P   = 290, # 0124h, kW L1, Watt*10
    L1_SCHEINLEISTUNG_S = 292, # 0126h, kVA L1, VA*10
    L1_BLINDLEISTUNG_Q  = 294, # 0128h, kvar L1, var*10