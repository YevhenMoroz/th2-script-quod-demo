from enum import Enum


class ExecutionReportConst(Enum):
    TransExecStatus_FIL = 'FIL'
    TransExecStatus_PFL = 'PFL'
    ExecType_TRD = 'TRD'
    ExecType_CAL = 'CAL'


class BasketMessagesConst(Enum):
    ListExecutionPolicy_C = 'C'
    ListOrderStatus_EXE = 'EXE'


class OrderReplyConst(Enum):
    PostTradeStatus_RDY = 'RDY'
    PostTradeStatus_BKD = 'BKD'
    DoneForDay_YES = "Y"
    TransStatus_OPN = 'OPN'
    DiscloseExec_R = 'R'
    DiscloseExec_M = 'M'
    TransStatus_SEN = 'SEN'
    OrdStatus_HLD = 'HLD'
    ExecStatus_OPN = 'OPN'


class ExecutionPolicyConst(Enum):
    DMA = 'D'
    CARE = 'C'


class SubmitRequestConst(Enum):
    USER_ROLE_1 = "TRA"
    OrdCapacity_Agency = 'Agency'


class AllocationReportConst(Enum):
    AllocStatus_ACK = 'ACK'
    MatchStatus_MAT = 'MAT'
    AllocSummaryStatus_MAG = 'MAG'
    AllocStatus_APP = 'APP'
    AllocStatus_CXL = 'CXL'


class AllocationInstructionConst(Enum):
    SettlType_REG = 'REG'
    RootMiscFeeType_EXC = 'EXC'
    CommissionAmountType_BRK = 'BRK'
    COMM_AND_FEES_BASIS_A = 'A'
    COMM_AND_FEES_BASIS_UNI = 'UNI'
    ConfirmationService_MAN = 'MAN'


class ConfirmationReportConst(Enum):
    ConfirmStatus_AFF = 'AFF'
    MatchStatus_MAT = 'MAT'
    ConfirmStatus_CXL = 'CXL'
    MatchStatus_UNM = 'UNM'


class CommissionBasisConst(Enum):
    CommissionBasis_ABS = 'ABS'


class CommissionAmountTypeConst(Enum):
    CommissionAmountType_BRK = 'BRK'


class OrdListNotificationConst(Enum):
    ListOrderStatus_EXE = 'EXE'
    OrderListWaveStatus_TER = 'TER'


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
    ConfirmationReportBlock = 'ConfirmationReportBlock'
    AffirmStatus = 'AffirmStatus'
    ConfirmationService = 'ConfirmationService'
    ClientAllocID = 'ClientAllocID'
    PostTradeStatus = 'PostTradeStatus'
    OrdUpdateBlock = 'OrdUpdateBlock'
    ComputeBookingFeesCommissionsReplyBlock = 'ComputeBookingFeesCommissionsReplyBlock'
    ComputeBookingFeesCommissionsRequestBlock = 'ComputeBookingFeesCommissionsRequestBlock'
    ClOrdID = 'ClOrdID'
    OrdReplyBlock = 'OrdReplyBlock'
    OrdStatus = 'OrdStatus'
    ExecType = 'ExecType'
    MatchStatus = 'MatchStatus'
    AllocStatus = 'AllocStatus'
    NewOrderListReplyBlock = 'NewOrderListReplyBlock'
    OrderListID = 'OrderListID'
    OrderListName = 'OrderListName'
    ListExecutionPolicy = 'ListExecutionPolicy'
    ListOrderStatus = 'ListOrderStatus'
    NewOrderSingleBlock = 'NewOrderSingleBlock'
    ClientCommissionDataBlock = 'ClientCommissionDataBlock'
    ClientCommission = 'ClientCommission'
    OrderBagNotificationBlock = 'OrderBagNotificationBlock'
    OrderBagName = 'OrderBagName'
    OrderBagID = 'OrderBagID'
    OrderBagQty = 'OrderBagQty'
    PegScope = 'PegScope'
    PegOffsetType = 'PegOffsetType'
    PegOffsetValue = 'PegOffsetValue'
    OrderBagWaveNotificationBlock = 'OrderBagWaveNotificationBlock'
    PegInstructionsBlock = 'PegInstructionsBlock'
    OrderBagWaveRequestBlock = 'OrderBagWaveRequestBlock'
    PositionReportBlock = 'PositionReportBlock'
    PositionList = 'PositionList'
    PositionBlock = 'PositionBlock'
    PositQty = 'PositQty'
    MiscFeesList = 'MiscFeesList'
    MiscFeesBlock = 'MiscFeesBlock'
    MiscFeeType = 'MiscFeeType'
    MiscFeeBasis = 'MiscFeeBasis'
    MiscFeeAmt = 'MiscFeeAmt'
    MiscFeeRate = 'MiscFeeRate'
    MiscFeeCurr = 'MiscFeeCurr'
    ExecutionPolicy = 'ExecutionPolicy'
    """List Wave"""
    OrderListWaveNotificationBlock = 'OrderListWaveNotificationBlock'
    OrderNotificationElements = "OrdNotificationElements"
    OrderListWaveStatus = 'OrderListWaveStatus'
    PercentQtyToRelease = 'PercentQtyToRelease'
    RouteID = 'RouteID'
    """External Algo"""
    ExternalAlgoParametersBlock = 'ExternalAlgoParametersBlock'
    ExternalAlgoParameterListBlock = 'ExternalAlgoParameterListBlock'
    ExternalAlgoParameterBlock = 'ExternalAlgoParameterBlock'
    AlgoParamString = 'AlgoParamString'
    AlgoParameterName = 'AlgoParameterName'
    VenueScenarioParameterID = 'VenueScenarioParameterID'
    ScenarioID = 'ScenarioID'
    ExternalAlgo = 'ExternalAlgo'



class JavaApiPartyRoleConstants(Enum):
    PartyRole_EXF = 'EXF'
    PartyRole_CNF = 'CNF'


class BagChildCreationPolicy(Enum):
    Split = 'SPL'


class TimeInForces(Enum):
    DAY = 'DAY'


class OrdTypes(Enum):
    Limit = 'LMT'


class PegScopes(Enum):
    Local = 'LOC'


class PegOffsetTypes(Enum):
    Price = 'PRC'
