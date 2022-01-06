from enum import Enum


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class ListingID(Enum):
    PAR_VETO = "1200"


class InstrID(Enum):
    PAR = "5XRAA7DXZg14IOkuNrAfsg"


class QtyPercentageProfile(Enum):
    RemainingQty = "REM"
    InitialQty = "INI"
    TargetBasketQty = "TAB"
