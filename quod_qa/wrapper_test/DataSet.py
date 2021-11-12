from enum import Enum


class DirectionEnum(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"


class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"


class Instrument(Enum):
    FR0010436584 = dict(
            Symbol='FR0010436584',
            SecurityID='FR0010436584',
            SecurityIDSource='4',
            SecurityExchange='XPAR'
        )
    test = dict(
            Symbol='FR0010436000',
            SecurityID='FR0010436000',
            SecurityIDSource='4',
            SecurityExchange='XPAR'
        )
    FR0000062788 = dict(
        Symbol='FR0000062788_EUR',
        SecurityID='FR0000062788',
        SecurityIDSource='4',
        SecurityExchange='XPAR'
    )


class Connectivity(Enum):
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_317_ss = "fix-sell-317-standard-test"
    Ganymede_317_buy = "fix-buy-317-standard-test"
