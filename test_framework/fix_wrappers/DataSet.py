from enum import Enum


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"
    MarketDataRequest = "MarketDataRequest"
    MarketDataIncrementalRefresh = "MarketDataIncrementalRefresh"
    MarketDataSnapshotFullRefresh = "MarketDataSnapshotFullRefresh"
    NewOrderList = "NewOrderList"
    ListStatus = "ListStatus"
    QuoteRequest = "QuoteRequest"
    Quote = "Quote"
    Confirmation = "Confirmation"
    AllocationInstruction = "AllocationInstruction"


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
    BUI = dict(
        Symbol='BUI',
        SecurityID='FR0000062788',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    PAR = dict(
        Symbol='PAR',
        SecurityID='FR0010263202',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    ISI1 = dict(
        Symbol='ISI1',
        SecurityID='ISI1',
        SecurityIDSource='4',
        SecurityExchange='XEUR',
        SecurityType='CS'
    )
    FR0004186856 = dict(
        Symbol='FR0004186856_EUR',
        SecurityID='FR0004186856',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )


class Connectivity(Enum):
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_316_Feed_Handler = 'fix-feed-handler-316-ganymede'
    Ganymede_316_Sell_Side = 'fix-sell-side-316-ganymede'
    Ganymede_316_Buy_Side = 'fix-buy-side-316-ganymede'
    Ganymede_317_ss = 'fix-sell-317-standard-test'
    Ganymede_317_bs = 'fix-buy-317-standard-test'
    Ganymede_317_dc = 'fix-sell-317-backoffice'
    Ganymede_317_wa = "rest_wa317ganymede"


class GatewaySide(Enum):
    Sell = "Sell"
    Buy = "Buy"


class Status(Enum):
    Pending = "Pending"
    New = "New"
    Fill = "Fill"
    PartialFill = "PartialFill"
    CancelRequest = "CancelReplace"
    Cancel = "Cancel"


class CommissionClients(Enum):
    CLIENT_COMM_1 = "CLIENT_COMM_1"
    CLIENT_COMM_2 = "CLIENT_COMM_2"


class CommissionAccounts(Enum):
    CLIENT_COMM_1_SA1 = "CLIENT_COMM_1_SA1"
    CLIENT_COMM_1_SA2 = "CLIENT_COMM_1_SA2"
    CLIENT_COMM_1_SA3 = "CLIENT_COMM_1_SA3"
    CLIENT_COMM_2_SA1 = "CLIENT_COMM_2_SA1"
    CLIENT_COMM_2_SA2 = "CLIENT_COMM_2_SA2"
    CLIENT_COMM_2_SA3 = "CLIENT_COMM_2_SA3"


class FeeTypes(Enum):
    Agent = "AGE"
    ExchFees = "EXC"
    Levy = "LEV"
    ConsumptionTax = "CTX"
    Conversion = "CON"
    Extra = "EXT"
    LocalComm = "LOC"
    Markup = "MAR"
    Other = "OTH"
    PerTransac = "TRA"
    Regulatory = "REG"
    Route = "ROU"
    Stamp = "STA"
    Tax = "TAX"
    ValueAddedTax = "VAT"


class FeesAndCommissions(Enum):
    Fee1 = 1
    Fee2 = 2
    Fee3 = 3
    Commission1 = 1
    Commission2 = 2
    Commission3 = 3


class CommissionProfiles(Enum):
    Abs_Amt = 1
    PerU_Qty = 2
    Perc_Qty = 3
    Perc_Amt = 4
    Bas_Amt = 5
    Bas_Qty = 6
