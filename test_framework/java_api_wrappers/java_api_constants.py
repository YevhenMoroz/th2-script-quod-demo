from enum import Enum


class ExecutionReportConst(Enum):
    TransExecStatus_FIL = 'FIL'
    TransExecStatus_PFL = 'PFL'
    ExecType_TRD = 'TRD'
    ExecType_CAL = 'CAL'
    ExecType_CAN = 'CAN'
    ExecType_DFD = 'DFD'
    ExecType_ACT = 'ACT'
    PostTradeExecStatus_NAL = 'NAL'


class BasketMessagesConst(Enum):
    ListExecutionPolicy_C = 'C'
    ListOrderStatus_EXE = 'EXE'
    ListOrderStatus_REJ = 'REJ'


class BagMessagesConst(Enum):
    OrderBagStatus_NEW = 'NEW'


class OrderReplyConst(Enum):
    PostTradeStatus_RDY = 'RDY'
    PostTradeStatus_BKD = 'BKD'
    DoneForDay_YES = "Y"
    TransStatus_OPN = 'OPN'
    DiscloseExec_R = 'R'
    DiscloseExec_M = 'M'
    TransStatus_SEN = 'SEN'
    OrdStatus_HLD = 'HLD'
    OrdStatus_REJ = 'REJ'
    OrdStatus_CXL = 'CXL'
    ExecStatus_OPN = 'OPN'
    TransStatus_CXL = 'CXL'
    TransStatus_TER = 'TER'
    TransStatus_ELI = 'ELI'
    TransStatus_REJ = 'REJ'
    OrdCapacity_A = 'A'
    OrdCapacity_P = 'P'
    OrdCapacity_I = 'I'
    IsLocked_Y = 'Y'
    IsLocked_N = 'N'
    ExecType_REP = 'REP'
    ExecType_PCA = 'PCA'
    ExecType_PMO = 'PMO'


class ExecutionPolicyConst(Enum):
    DMA = 'D'
    CARE = 'C'
    Synthetic = 'S'


class SubmitRequestConst(Enum):
    USER_ROLE_1 = "TRA"
    OrdCapacity_Agency = 'Agency'
    Side_Buy = 'Buy'
    Side_B_aka_Buy = 'B'
    Side_Sell = 'Sell'


class AllocationReportConst(Enum):
    AllocStatus_ACK = 'ACK'
    MatchStatus_MAT = 'MAT'
    AllocSummaryStatus_MAG = 'MAG'
    AllocStatus_APP = 'APP'
    AllocStatus_CXL = 'CXL'
    AllocReportType_ACC = 'ACC'
    ConfirmationService_EXT = 'EXT'
    ConfirmationService_MAN = 'MAN'
    SettlCurrFxRateCalc_Multiply = 'Multiply'
    SettlCurrFxRateCalc_Devide = 'Devide'
    ConfirmationService_INT = 'INT'


class AllocationInstructionConst(Enum):
    SettlType_REG = 'REG'
    RootMiscFeeType_EXC = 'EXC'
    CommissionAmountType_BRK = 'BRK'
    COMM_AND_FEES_BASIS_A = 'A'
    COMM_AND_FEES_BASIS_P = 'P'
    COMM_AND_FEES_BASIS_UNI = 'UNI'
    COMM_AND_FEES_BASIS_PERCENTAGE = 'PCT'
    COMM_AND_FEES_TYPE_AGE = "AGE"
    ConfirmationService_MAN = 'MAN'
    COMM_AND_FEE_BASIS_ABS = 'ABS'
    COMM_AND_FEE_BASIS_BPS = 'BPS'
    COMM_AND_FEE_TYPE_TRA = 'TRA'  # PerTransac
    COMM_AND_FEE_TYPE_LEV = 'LEV'  # Levy
    COMM_AND_FEE_TYPE_STA = 'STA'  # STA
    COMM_AND_FEE_BASIS_PCT = 'PCT'
    ComputeFeesCommissions_Y = 'Y'
    ComputeFeesCommissions_N = 'N'
    COMM_AMD_FEE_TYPE_REG = "REG"
    CommissionAmountSubType_OTH = 'OTH'
    RootMiscFeeCategory_OTH = 'OTH'
    BookingType_CFD = 'CFD'
    NetGrossInd_N = 'N'
    SettlCurrFxRateCalc_M = 'M'
    SettlCurrFxRateCalc_D = 'D'


class ConfirmationReportConst(Enum):
    ConfirmStatus_AFF = 'AFF'
    MatchStatus_MAT = 'MAT'
    ConfirmStatus_CXL = 'CXL'
    MatchStatus_UNM = 'UNM'
    AffirmStatus_AFF = 'AFF'
    ConfirmTransType_NEW = 'NEW'
    ConfirmTransType_CAN = 'CAN'


class CommissionBasisConst(Enum):
    CommissionBasis_ABS = 'ABS'
    CommissionBasis_PCT = 'PCT'
    CommissionBasis_BPS = 'BPS'
    CommissionBasis_UNI = 'UNI'


class CommissionAmountTypeConst(Enum):
    CommissionAmountType_BRK = 'BRK'


class OrdListNotificationConst(Enum):
    ListOrderStatus_EXE = 'EXE'
    OrderListWaveStatus_TER = 'TER'
    OrderListWaveStatus_NEW = 'NEW'


class QtyPercentageProfile(Enum):
    RemainingQty = "REM"
    InitialQty = "INI"
    TargetBasketQty = "TAB"


class JavaApiFields(Enum):
    ExecCommission = 'ExecCommission'
    TransExecStatus = 'TransExecStatus'
    TransStatus = 'TransStatus'
    ExecutionReportBlock = 'ExecutionReportBlock'
    CounterpartList = "CounterpartList"
    CounterpartBlock = "CounterpartBlock"
    PartyRole = "PartyRole"
    CounterpartID = "CounterpartID"
    OrderNotificationBlock = "OrdNotificationBlock"
    OrdID = 'OrdID'
    TimeInForce = 'TimeInForce'
    ExpireDate = 'ExpireDate'
    ExecID = 'ExecID'
    AllocationReportBlock = 'AllocationReportBlock'
    ConfirmationReportBlock = 'ConfirmationReportBlock'
    AffirmStatus = 'AffirmStatus'
    ConfirmationService = 'ConfirmationService'
    ClientAllocID = 'ClientAllocID'
    PostTradeStatus = 'PostTradeStatus'
    OrdUpdateBlock = 'OrdUpdateBlock'
    ComputeBookingFeesCommissionsRequestBlock = 'ComputeBookingFeesCommissionsRequestBlock'
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
    OrderBagNotificationBlock = 'OrderBagNotificationBlock'
    OrderBagName = 'OrderBagName'
    OrderBagID = 'OrderBagID'
    OrderBagQty = 'OrderBagQty'
    ReleasedQty = 'ReleasedQty'
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
    ManualDayCumAmt = 'ManualDayCumAmt'
    ManualDayCumQty = 'ManualDayCumQty'
    AllocReportType = 'AllocReportType'
    RootMiscFeesList = 'RootMiscFeesList'
    DayCumQty = 'DayCumQty'
    DayCumAmt = 'DayCumAmt'
    UnsolicitedOrder = "UnsolicitedOrder"
    OrdQty = 'OrdQty'
    LeavesQty = 'LeavesQty'
    CumQty = 'CumQty'
    UnmatchedQty = 'UnmatchedQty'
    ExecPrice = 'ExecPrice'
    DisclosedExec = 'DisclosedExec'
    OrdListNotificationBlock = 'OrdListNotificationBlock'
    AddOrdersToOrderListReplyBlock = 'AddOrdersToOrderListReplyBlock'
    RemoveOrdersFromOrderListReplyBlock = 'RemoveOrdersFromOrderListReplyBlock'
    AccountGroupName = 'AccountGroupName'
    PreTradeAllocationBlock = 'PreTradeAllocationBlock'
    PreTradeAllocationList = 'PreTradeAllocationList'
    PreTradeAllocAccountBlock = 'PreTradeAllocAccountBlock'
    AllocAccountID = 'AllocAccountID'
    SuspendOrderManagementReplyBlock = 'SuspendOrderManagementReplyBlock'
    TradeEntryReplyBlock = 'TradeEntryReplyBlock'
    OrdNotificationBlock = 'OrdNotificationBlock'
    OrderModificationReplyBlock = 'OrderModificationReplyBlock'
    CDTransferReplyBlock = 'CDTransferReplyBlock'
    CDTransferID = 'CDTransferID'
    RecipientUserID = 'RecipientUserID'
    RecipientDeskID = 'RecipientDeskID'
    CDOrdNotifBlock = 'CDOrdNotifBlock'
    CDOrdNotifID = 'CDOrdNotifID'
    CDRequestType = 'CDRequestType'
    OrderModificationNotificationBlock = 'OrderModificationNotificationBlock'
    ReportedCumQty = 'ReportedCumQty'
    Ord = 'Ord'
    GatingRuleID = 'GatingRuleID'
    GatingRuleCondName = 'GatingRuleCondName'
    ParentOrdrList = 'ParentOrdrList'
    """List Wave"""
    OrderListWaveNotificationBlock = 'OrderListWaveNotificationBlock'
    OrderNotificationElements = "OrdNotificationElements"
    OrderListWaveStatus = 'OrderListWaveStatus'
    PercentQtyToRelease = 'PercentQtyToRelease'
    QtyPercentageProfile = 'QtyPercentageProfile'
    RootParentOrdID = 'RootParentOrdID'
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
    VenueScenarioID = 'VenueScenarioID'
    NewOrderReplyBlock = 'NewOrderReplyBlock'
    OrdType = 'OrdType'
    VenueID = 'VenueID'
    AlgoParametersBlock = 'AlgoParametersBlock'
    AlgoType = 'AlgoType'

    ComputeBookingFeesCommissionsReplyBlock = 'ComputeBookingFeesCommissionsReplyBlock'
    RootMiscFeeBasis = 'RootMiscFeeBasis'
    RootMiscFeeRate = 'RootMiscFeeRate'
    RootMiscFeeCurr = 'RootMiscFeeCurr'
    RootMiscFeeType = 'RootMiscFeeType'
    RootMiscFeeAmt = 'RootMiscFeeAmt'
    RootMiscFeesBlock = 'RootMiscFeesBlock'
    CommissionBasis = 'CommissionBasis'
    CommissionAmountType = 'CommissionAmountType'
    CommissionRate = 'CommissionRate'
    CommissionCurrency = 'CommissionCurrency'
    CommissionAmount = 'CommissionAmount'
    ClientCommissionList = 'ClientCommissionList'
    ClientCommissionBlock = 'ClientCommissionBlock'
    AllocReportID = 'AllocReportID'
    AllocInstructionID = 'AllocInstructionID'
    AllocType = 'AllocType'
    AllocTransType = 'AllocTransType'
    AllocStatus = 'AllocStatus'
    ConfirmStatus = 'ConfirmStatus'
    MatchStatus = 'MatchStatus'
    AllocSummaryStatus = 'AllocSummaryStatus'
    DoneForDay = 'DoneForDay'
    NetMoney = 'NetMoney'
    NetPrice = 'NetPrice'
    AllocQty = 'AllocQty'
    BookingAllocInstructionID = 'BookingAllocInstructionID'
    ClBookingRefID = 'ClBookingRefID'
    AvgPrice = 'AvgPrice'
    GrossTradeAmt = 'GrossTradeAmt'
    AvgPx = 'AvgPx'
    SettlLocationID = 'SettlLocationID'
    SettlementModelID = 'SettlementModelID'
    Qty = 'Qty'
    Side = 'Side'
    AllocationInstructionQtyList = 'AllocationInstructionQtyList'
    AllocationInstructionQtyBlock = 'AllocationInstructionQtyBlock'
    BookingQty = 'BookingQty'
    WashBookAccountID = 'WashBookAccountID'
    SettlCurrency = 'SettlCurrency'
    SettlCurrAmt = 'SettlCurrAmt'
    SettlCurrFxRate = 'SettlCurrFxRate'
    SettlCurrFxRateCalc = 'SettlCurrFxRateCalc'
    CommissionAmountSubType = 'CommissionAmountSubType'
    ConfirmationID = 'ConfirmationID'
    RootMiscFeeCategory = 'RootMiscFeeCategory'
    ClAllocID = 'ClAllocID'
    AccountGroupID = 'AccountGroupID'
    ConfirmTransType = 'ConfirmTransType'
    SingleAllocAccountID = 'SingleAllocAccountID'
    OrdCapacity = 'OrdCapacity'
    CDOrdFreeNotes = 'CDOrdFreeNotes'
    VenueClientActGrpName = 'VenueClientActGrpName'
    IsLocked = 'IsLocked'
    Currency = "Currency"
    FreeNotes = 'FreeNotes'
    Price = 'Price'
    VenueClientAccountName = 'VenueClientAccountName'
    PostTradeExecStatus = 'PostTradeExecStatus'
    DiscloseExec = 'DiscloseExec'
    DayAvgPrice = 'DayAvgPrice'
    SuspendedCare = "SuspendedCare"
    SubCounterpartList = "SubCounterpartList"

    ManualOrderCrossReplyBlock = "ManualOrderCrossReplyBlock"
    # fields of Bag
    OrderBagStatus = 'OrderBagStatus'
    OrderWaveStatus = 'OrderWaveStatus'
    OrderBagExecStatus = 'OrderBagExecStatus'


class JavaApiPartyRoleConstants(Enum):
    PartyRole_EXF = 'EXF'
    PartyRole_CNF = 'CNF'


class BagChildCreationPolicy(Enum):
    Split = 'SPL'
    Group = "GRP"
    AVP = 'AVP'  # GroupByAvgPx


class TimeInForces(Enum):
    DAY = 'DAY'
    GTD = 'GTD'
    ATC = 'ATC'


class OrdTypes(Enum):
    Limit = 'LMT'
    Market = 'MKT'


class PegScopes(Enum):
    Local = 'LOC'


class PegOffsetTypes(Enum):
    Price = 'PRC'


class AllocTransTypes(Enum):
    AllocTransType_Replace = "R"


class AllocTypes(Enum):
    AllocType_P = 'Preliminary'


class OrderBagConst(Enum):
    OrderBagStatus_NEW = 'NEW'
    OrderBagStatus_CXL = 'CXL'
    OrderWaveStatus_TER = 'TER'
    OrderBagStatus_TER = 'TER'


class CDResponsesConst(Enum):
    CDRequestType_MOD = 'MOD'
    CDRequestType_CAN = 'CAN'
