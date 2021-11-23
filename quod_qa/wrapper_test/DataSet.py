from enum import Enum


class DirectionEnum(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"


class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"
    NewOrderList = "NewOrderList"
    ListStatus = "ListStatus"


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
    ISI1 = dict(
        Symbol='ISI1',
        SecurityID='ISI1',
        SecurityIDSource='4',
        SecurityExchange='XEUR'
    )

    ISI3 = dict(
        Symbol='ISI3',
        SecurityID='ISI3',
        SecurityIDSource='4',
        SecurityExchange='XEUR'

    )


class Connectivity(Enum):
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_317_ss = 'fix-sell-317-standard-test'
    Ganymede_317_bs = 'fix-buy-317-standard-test'
    Ganymede_317_dc = 'fix-sell-317-backoffice'
    Ganymede_317_wa_rest = "rest_wa317ganymede"


class CommissionClientsAccounts(Enum):
    CLIENT_COMM_1 = "CLIENT_COMM_1"
    CLIENT_COMM_2 = "CLIENT_COMM_2"
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
    pass
