from enum import Enum


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class ORSMessages(Enum):
    OrderSubmit = 'Order_OrderSubmit'
    TradeEntryRequest = 'Order_TradeEntryRequest'
    OrderListWaveCreationRequest = 'Order_OrderListWaveCreationRequest'
    UnMatchRequest = 'Order_UnMatchRequest'
    ManualOrderCrossRequest = 'Order_ManualOrderCrossRequest'


class Listing(Enum):
    PAR_VETO = {'ListingBlock': [{'ListingID': "1200"}]}


class InstrID(Enum):
    PAR = "5XRAA7DXZg14IOkuNrAfsg"
