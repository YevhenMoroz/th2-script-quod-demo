from enum import Enum


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    NewOrderMultiLeg = "NewOrderMultileg"
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
        SecurityType='CS',
        SecurityDesc='DREAMNEX'
    )
    FR0000121121 = dict(
        Symbol='FR0000121121',
        SecurityID='FR0000121121',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS',
        SecurityDesc='EURAZEO'
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
    DUMMY = dict(
        Symbol='DUMMY',
        SecurityID='DUMMY',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    ISI3 = dict(
        Symbol='ISI3',
        SecurityID='ISI3',
        SecurityIDSource='4',
        SecurityExchange='XEUR',
        SecurityType='CS'
    )
    RF = dict(
        Symbol='FR0000121121_EUR',
        SecurityID='FR0000121121',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    SOCM = dict(
        Symbol='FR0000037210_EUR',
        SecurityID='FR0000037210',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )


class Connectivity(Enum):
    Ganymede_316_Feed_Handler = 'fix-feed-handler-316-ganymede'
    Ganymede_316_Sell_Side = 'fix-sell-side-316-ganymede'
    Ganymede_316_Buy_Side = 'fix-buy-side-316-ganymede'
    Ganymede_316_Buy_Side_Redburn = 'fix-buy-side-316-ganymede-redburn'
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_317_ss = 'fix-sell-317-standard-test'
    Ganymede_317_bs = 'fix-buy-317-standard-test'
    Ganymede_317_dc = 'fix-sell-317-backoffice'
    Ganymede_317_wa = "rest_wa317ganymede"
    Luna_314_ss_rfq = 'fix-ss-rfq-314-luna-standard'
    Luna_314_bs_rfq = 'fix-bs-rfq-314-luna-standard'
    Luna_314_ss_esp = 'fix-sell-esp-m-314luna-stand'
    Luna_314_ss_esp_t = 'fix-sell-esp-t-314-stand'
    Luna_314_Feed_Handler = 'fix-fh-314-luna'
    Luna_314_Feed_Handler_Q = 'fix-fh-q-314-luna'
    Luna_314_dc = 'fix-sell-m-314luna-drop'
    Luna_314_wa = "rest_wa314luna"
    Kratos_309_ss_rfq = 'fix-sell-rfq-m-309kratos-stand'
    Kratos_309_bs_rfq = 'fix-bs-rfq-309-kratos-stand'
    Kratos_309_ss_esp = 'fix-sell-esp-m-309kratos-stand'
    Kratos_309_bs_esp = 'fix-bs-esp-309-kratos-stand'
    Kratos_309_Feed_Handler = 'fix-fh-309-kratos'
    Ganymede_317_ja = '317_java_api'
    Ganymede_317_als_email_report = 'log317-als-email-report'
    Columbia_310_Feed_Handler = 'fix-fh-310-columbia'
    Columbia_310_Sell_Side = 'fix-ss-310-columbia-standart'
    Columbia_310_Buy_Side = 'fix-bs-310-columbia'


class GatewaySide(Enum):
    Sell = "Sell"
    Buy = "Buy"


class Status(Enum):
    Pending = "Pending"
    New = "New"
    Fill = "Fill"
    PartialFill = "PartialFill"
    Reject = "Reject"
    CancelRequest = "CancelReplace"
    Cancel = "Cancel"
    Eliminate = "Eliminate"


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
    CLIENT_COMM_1_EXEMPTED = "CLIENT_COMM_1_EXEMPTED"


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


class Fees(Enum):
    Fee1 = 1
    Fee2 = 2
    Fee3 = 3


class Commissions(Enum):
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
    Abs_Amt_USD = 7
    Abs_Amt_2 = 8


class ExecScope(Enum):
    AllExec = "ALL"
    DayFirstExec = "DAF"
    FirstExec = "FST"


class TimeInForce(Enum):
    Day = 0
    GoodTillCancel = 1
    AtTheOpening = 2
    ImmediateOrCancel = 3
    FillOrKill = 4
    GoodTillCrossing = 5
    GoodTillDate = 6
    AtTheClose = 7
    ValidForAuction = 100


class FreeNotesReject(Enum):
    MissWouldPriceReference = "missing WouldPriceReference"
    MissLimitPriceReference = "missing LimitPriceReference"
    MissNavigatorLimitPriceReference = "missing NavigatorLimitPriceReference"
    MissNavigatorLimitPrice = "missing Limit price for Navigator"
    InvalidMaxParticipation = "invalid value for MaxParticipation"
    InvalidPercentageOfVolume = "invalid value for percentage of volume"
    InvalidPricePoint1Participation = "invalid value for PricePoint1Participation"
    InvalidPricePoint2Participation = "invalid value for PricePoint2Participation"


class Reference(Enum):
    LastTradePrice = 'LTP'
    Primary = 'PRM'
    Market = 'MKT'
    Mid = 'MID'
    Open = 'OPN'
    Close = 'CLO'
    DayHight = 'DHI'
    DayLow = 'DLO'
    Manual = 'MAN'
    Limit = 'LMT'
