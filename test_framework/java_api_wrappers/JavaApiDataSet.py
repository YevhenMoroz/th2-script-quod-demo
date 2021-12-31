from enum import Enum


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class ORSMessages(Enum):
    OrderSubmit = 'Order_OrderSubmit'
    TradeEntry = 'Order_TradeEntryRequest'
    OrderListWaveCreation = 'Order_OrderListWaveCreationRequest'
    UnMatch = 'Order_UnMatchRequest'
    ManualOrderCross = 'Order_ManualOrderCrossRequest'


class Listing(Enum):
    PAR_VETO = {'ListingBlock': [{'ListingID': "1200"}]}


class InstrID(Enum):
    PAR = "5XRAA7DXZg14IOkuNrAfsg"
