from enum import Enum

class FreeNotesReject(Enum):
    MissWouldPriceReference = "missing WouldPriceReference"
    MissLimitPriceReference = "missing LimitPriceReference"