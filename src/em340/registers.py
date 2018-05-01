from enum import IntEnum

class Registers(IntEnum):
    SYS_WIRKLEISTUNG_P = 262,  # 0106h, kW sys, Watt*10
    SYS_WIRKLEISTUNG_S = 264,  # 0108h, kVA sys, VA*10
    SYS_WIRKLEISTUNG_Q = 266,  # 010Ah, kvar sys, var*10

    # Phase 1
    L1_WIRKLEISTUNG_P   = 292, # 0124h, kW L1, Watt*10
    L1_SCHEINLEISTUNG_S = 294, # 0126h, kVA L1, VA*10
    L1_BLINDLEISTUNG_Q  = 296, # 0128h, kvar L1, var*10

    # note: 1 W = 1 var = 1 VA