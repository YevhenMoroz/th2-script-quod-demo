from enum import Enum


class ExecutionReportConst(Enum):
    TransExecStatus_FIL = 'FIL'
    TransExecStatus_PFL = 'PFL'


class BasketMessagesConst(Enum):
    ListExecutionPolicy_C = 'C'
    ListOrderStatus_EXE = 'EXE'


class OrderReplyConst(Enum):
    PostTradeStatus_RDY = 'RDY'
    PostTradeStatus_BKD = 'BKD'
    DoneForDay_YES = "Y"
    TransStatus_OPN = 'OPN'
    OrdStatus_HLD = 'HLD'
    ExecStatus_OPN = 'OPN'


class SubmitRequestConst(Enum):
    USER_ROLE_1 = "TRA"
    OrdCapacity_Agency = 'Agency'


class AllocationReportConst(Enum):
    AllocStatus_ACK = 'ACK'
    MatchStatus_MAT = 'MAT'
    AllocSummaryStatus_MAG = 'MAG'


class AllocationInstructionConst(Enum):
    SettlType_REG = 'REG'
    RootMiscFeeType_EXC = 'EXC'
    CommissionAmountType_BRK = 'BRK'
    COMM_AND_FEES_BASIS_A = 'A'
    COMM_AND_FEES_BASIS_UNI = 'UNI'


class ConfirmationReportConst(Enum):
    ConfirmStatus_AFF = 'AFF'
    MatchStatus_MAT = 'MAT'
    ConfirmStatus_CXL = 'CXL'
    MatchStatus_UNM = 'UNM'


class CommissionBasisConst(Enum):
    CommissionBasis_ABS = 'ABS'


class CommissionAmountTypeConst(Enum):
    CommissionAmountType_BRK = 'BRK'


class QtyPercentageProfile(Enum):
    RemainingQty = "REM"
    InitialQty = "INI"
    TargetBasketQty = "TAB"


class JavaApiFields(Enum):
    TransExecStatus = 'TransExecStatus'
    TransStatus = 'TransStatus'
    ExecutionReportBlock = 'ExecutionReportBlock'
    CounterpartList = "CounterpartList"
    CounterpartBlock = "CounterpartBlock"
    PartyRole = "PartyRole"
    OrderNotificationBlock = "OrdNotificationBlock"
    OrdID = 'OrdID'
    ExecID = 'ExecID'
    AllocationReportBlock = 'AllocationReportBlock'
    ClientAllocID = 'ClientAllocID'
    PostTradeStatus = 'PostTradeStatus'
    OrdUpdateBlock = 'OrdUpdateBlock'
    ClOrdID = 'ClOrdID'
    OrdReplyBlock = 'OrdReplyBlock'
    OrdStatus = 'OrdStatus'
    ExecType = 'ExecType'
    NewOrderListReplyBlock = 'NewOrderListReplyBlock'
    OrderListID = 'OrderListID'
    OrderListName = 'OrderListName'
    ListExecutionPolicy = 'ListExecutionPolicy'
    ListOrderStatus = 'ListOrderStatus'
    NewOrderSingleBlock = 'NewOrderSingleBlock'
    ClientCommissionDataBlock = 'ClientCommissionDataBlock'
    ClientCommission = 'ClientCommission'


class JavaApiPartyRoleConstants(Enum):
    PartyRole_EXF = 'EXF'
    PartyRole_CNF = 'CNF'
