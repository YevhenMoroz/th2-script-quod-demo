from enum import Enum


class DirectionEnum(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"


class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"
    MarketDataRequest = "MarketDataRequest"
    MarketDataIncrementalRefresh = "MarketDataIncrementalRefresh"
    MarketDataSnapshotFullRefresh = "MarketDataSnapshotFullRefresh"


class Instrument(Enum):
    FR0010436584 = dict(
        Symbol='FR0010436584',
        SecurityID='FR0010436584',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    test = dict(
        Symbol='FR0010436000',
        SecurityID='FR0010436000',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    FR0000062788 = dict(
        Symbol='FR0000062788_EUR',
        SecurityID='FR0000062788',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    FR0010263202 = dict(
        Symbol='FR0010263202_EUR',
        SecurityID='FR0010263202',
        SecurityIDSource='4',
        SecurityExchange='XPAR'
    )


class Connectivity(Enum):
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_316_Feed_Handler = 'fix-feed-handler-316-ganymede'
    Ganymede_316_Sell_Side = 'fix-sell-side-316-ganymede'
    Ganymede_316_Buy_Side = 'fix-buy-side-316-ganymede'
