from enum import Enum


class ExecutionReportConst(Enum):
    TransExecStatus_FIL = 'FIL'


class OrderReplyConst(Enum):
    PostTradeStatus_RDY = 'RDY'
    PostTradeStatus_BKD = 'BKD'
    DoneForDay_YES = "Y"
    TransStatus_OPN = 'OPN'


class SubmitRequestConst(Enum):
    USER_ROLE_1 = "TRA"
    OrdCapacity_Agency = 'Agency'


class AllocationReportConst(Enum):
    AllocStatus_ACK = 'ACK'
    MatchStatus_MAT = 'MAT'
    AllocSummaryStatus_MAG = 'MAG'


class AllocationInstructionConst(Enum):
    SettlType_REG = 'REG'


class ConfirmationReportConst(Enum):
    ConfirmStatus_AFF = 'AFF'
    MatchStatus_MAT = 'MAT'


class CommissionBasisConst(Enum):
    CommissionBasis_ABS = 'ABS'


class CommissionAmountTypeConst(Enum):
    CommissionAmountType_BRK = 'BRK'
