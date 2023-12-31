from enum import Enum


class ExecutionReportConst(Enum):
    TransExecStatus_FIL = 'FIL'
    TransExecStatus_PFL = 'PFL'
    ExecType_TRD = 'TRD'
    ExecType_CAL = 'CAL'
    ExecType_CAN = 'CAN'
    ExecType_DFD = 'DFD'
    ExecType_ACT = 'ACT'
    ExecType_POS = 'POS'
    PostTradeExecStatus_NAL = 'NAL'
    MiscFeeType_EXC = 'EXC'
    MiscFeeType_AGE = 'AGE'
    MiscFeeBasis_P = 'P'
    MiscFeeBasis_B = 'B'
    MiscFeeBasis_A = 'A'
    LastCapacity_Principal = 'P'
    LastCapacity_Principal_FULL_VALUE = 'Principal'
    LastCapacity_Agency_FULL_VALUE = 'Agency'
    LastCapacity_Mixed_FULL_VALUE = 'Mixed'
    LastCapacity_CrossAsMixed_FULL_VALUE = 'CrossAsMixed'
    LastCapacity_Agency = 'A'

    ExecOrigin_M = 'M'
    ExecOrigin_E = 'E'
    ExecType_Trade = 'Trade'
    ExecType_Replaced = 'Replaced'


class BasketMessagesConst(Enum):
    ListExecutionPolicy_C = 'C'
    ListOrderStatus_EXE = 'EXE'
    ListOrderStatus_REJ = 'REJ'
    ListOrderStatus_DON = 'DON'
    ListOrderStatus_CAN = 'CAN'


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
    OrdStatus_SUB = 'SUB'
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
    ExecType_CXL = 'CXL'
    ExecType_COR = 'COR'
    ExecType_PDO = 'PDO'
    ExecType_OPN = 'OPN'
    ExecType_RES = 'RES'
    CustOrderHandlingInst_LOC = 'LOC'


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
    PositionEffect_R = 'R'


class AllocationReportConst(Enum):
    AllocStatus_ACK = 'ACK'
    MatchStatus_MAT = 'MAT'
    MatchStatus_UNM = 'UNM'
    AllocSummaryStatus_MAG = 'MAG'
    AllocStatus_APP = 'APP'
    AllocStatus_REC = 'REC'
    AllocStatus_CXL = 'CXL'
    AllocReportType_ACC = 'ACC'
    ConfirmationService_EXT = 'EXT'
    ConfirmationService_MAN = 'MAN'
    SettlCurrFxRateCalc_Multiply = 'Multiply'
    SettlCurrFxRateCalc_Devide = 'Devide'
    ConfirmationService_INT = 'INT'


class AllocationInstructionConst(Enum):
    SettlType_REG = 'REG'
    SettlType_TOM = 'TOM'
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
    ListOrderStatus_DON = 'DON'
    OrderListWaveStatus_TER = 'TER'
    OrderListWaveStatus_NEW = 'NEW'
    OrderListWaveStatus_CXL = 'CXL'
    OrdStatus_SUB = 'SUB'


class QtyPercentageProfile(Enum):
    RemainingQty = "REM"
    InitialQty = "INI"
    TargetBasketQty = "TAB"


class JavaApiFields(Enum):
    ExecCommission = 'ExecCommission'
    SettlDate = 'SettlDate'
    ClearingTradePrice = 'ClearingTradePrice'
    HeldOrderAckReplyBlock = 'HeldOrderAckReplyBlock'
    AllocationInstructionBlock = 'AllocationInstructionBlock'
    RequestForOverdueRetailPositionsAckBlock = 'RequestForOverdueRetailPositionsAckBlock'
    TransExecStatus = 'TransExecStatus'
    BookingType = 'BookingType'
    OrdReportBlock = 'OrdReportBlock'
    LegOrderElements = 'LegOrderElements'
    Reason = 'Reason'
    LegOrderBlock = 'LegOrderBlock'
    LegNumber = 'LegNumber'
    LegInstrID = 'LegInstrID'
    OrdRejectedNotifBlock = 'OrdRejectedNotifBlock'
    LegPrice = 'LegPrice'
    MaxPriceLevels = 'MaxPriceLevels'
    MultiLegOrderModificationRequestBlock = 'MultiLegOrderModificationRequestBlock'
    PositionEffect = 'PositionEffect'
    NewOrderMultiLegBlock = 'NewOrderMultiLegBlock'
    BenchmarkList = 'BenchmarkList'
    BenchmarkBlock = 'BenchmarkBlock'
    StartBenchmarkTimestamp = 'StartBenchmarkTimestamp'
    EndBenchmarkTimestamp = 'EndBenchmarkTimestamp'
    RetailPositList = 'RetailPositList'
    BenchmarkNotificationBlock = 'BenchmarkNotificationBlock'
    RetailPositBlock = 'RetailPositBlock'
    CDOrdAckBatchRequestBlock = 'CDOrdAckBatchRequestBlock'
    HeldOrderAckBlock = 'HeldOrderAckBlock'
    HeldOrderAckType = 'HeldOrderAckType'
    ModifyChildren = 'ModifyChildren'
    CancelChildren = ' CancelChildren'
    PositionType = 'PositionType'
    StopPx = 'StopPx'
    TransactTime = 'TransactTime'
    ErrorMsg = "ErrorMsg"
    OrdModify = 'OrdModify'
    OrdModifyID = 'OrdModifyID'
    OverdueRetailPositList = 'OverdueRetailPositList'
    AccountID = 'AccountID'
    PosGoodTillDate = 'PosGoodTillDate'
    TransStatus = 'TransStatus'
    SecurityID = 'SecurityID'
    InstrSymbol = 'InstrSymbol'
    LeavesSellQty = 'LeavesSellQty'
    InstrumentBlock = 'InstrumentBlock'
    ExecutionReportBlock = 'ExecutionReportBlock'
    ManualOrderCrossRequestBlock = 'ManualOrderCrossRequestBlock'
    ReportVenueID = 'ReportVenueID'
    TradePublishIndicator = 'TradePublishIndicator'
    TradeReportTransType = 'TradeReportTransType'
    TargetAPA = 'TargetAPA'
    AssistedReportAPA = 'AssistedReportAPA'
    OnExchangeRequested = 'OnExchangeRequested'
    TradeCaptureReportNotifBlock = 'TradeCaptureReportNotifBlock'
    TradeReportID = 'TradeReportID'
    ManualOrderCrossID = 'ManualOrderCrossID'
    ManualOrderCrossTransType = 'ManualOrderCrossTransType'
    OrdID1 = 'OrdID1'
    OrdID2 = 'OrdID2'
    CounterpartList = "CounterpartList"
    CounterpartBlock = "CounterpartBlock"
    OrderModificationRequestBlock = 'OrderModificationRequestBlock'
    ClientAccountGroupID = 'ClientAccountGroupID'
    PartyRole = "PartyRole"
    CounterpartID = "CounterpartID"
    OrderNotificationBlock = "OrdNotificationBlock"
    OrdID = 'OrdID'
    VenueOrdID = 'VenueOrdID'
    PositionTransferInstructionBlock = 'PositionTransferInstructionBlock'
    TimeInForce = 'TimeInForce'
    ExpireDate = 'ExpireDate'
    ExecID = 'ExecID'
    AllocationReportBlock = 'AllocationReportBlock'
    UnrealizedPL = 'UnrealizedPL'
    ConfirmationReportBlock = 'ConfirmationReportBlock'
    ConfirmationBlock = 'ConfirmationBlock'
    Header = 'Header'
    Target = 'Target'
    Sender = 'Sender'
    TargetSubID = 'TargetSubID'
    TargetCompID = 'TargetCompID'
    SenderCompID = "SenderCompID"
    SenderSubID = "SenderSubID"
    CDOrdResponse = 'CDOrdResponse'
    AffirmStatus = 'AffirmStatus'
    OnBehalfOf = 'OnBehalfOf'
    OnBehalfOfCompID = "OnBehalfOfCompID"
    OnBehalfOfSubID = "OnBehalfOfSubID"
    DeliverToCompID = 'DeliverToCompID'
    DeliverToSubID = 'DeliverToSubID'
    ConfirmationService = 'ConfirmationService'
    ClientAllocID = 'ClientAllocID'
    PostTradeStatus = 'PostTradeStatus'
    MessageReply = 'MessageReply'
    MessageReplyBlock = 'MessageReplyBlock'
    OrdUpdateBlock = 'OrdUpdateBlock'
    ComputeBookingFeesCommissionsRequestBlock = 'ComputeBookingFeesCommissionsRequestBlock'
    ClOrdID = 'ClOrdID'
    OrdReplyBlock = 'OrdReplyBlock'
    ListingList = 'ListingList'
    CrossAnnouncementBlock = 'CrossAnnouncementBlock'
    CrossAnnouncementReplyBlock = 'CrossAnnouncementReplyBlock'
    CrossAnnouncementStatus = 'CrossAnnouncementStatus'
    CrossAnnouncementID = 'CrossAnnouncementID'
    EffectiveDate = 'EffectiveDate'
    CashAccountID = 'CashAccountID'
    OrdStatus = 'OrdStatus'
    ExecType = 'ExecType'
    VenueExecRefID = 'VenueExecRefID'
    NewOrderListReplyBlock = 'NewOrderListReplyBlock'
    OrderListID = 'OrderListID'
    OrderListName = 'OrderListName'
    ListExecutionPolicy = 'ListExecutionPolicy'
    ListOrderStatus = 'ListOrderStatus'
    NewOrderSingleBlock = 'NewOrderSingleBlock'
    StopPrice = 'StopPrice'
    PosValidity = 'PosValidity'
    ClientCommissionDataBlock = 'ClientCommissionDataBlock'
    ClientCommission = 'ClientCommission'
    OrderBagNotificationBlock = 'OrderBagNotificationBlock'
    ListingBlock = 'ListingBlock'
    ListingID = 'ListingID'
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
    MiscFeeCategory = 'MiscFeeCategory'
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
    RequestForPositionsAckBlock = 'RequestForPositionsAckBlock'
    InstrID = 'InstrID'
    CumBuyQty = 'CumBuyQty'
    CumSellQty = 'CumSellQty'
    GrossWeightedAvgPx = 'GrossWeightedAvgPx'
    NetWeightedAvgPx = 'NetWeightedAvgPx'
    DailyAgentFeeAmt = 'DailyAgentFeeAmt'
    DailyClientCommission = 'DailyClientCommission'
    QuarterToDateClientComm = 'QuarterToDateClientComm'
    DailyRealizedNetPL = 'DailyRealizedNetPL'
    DailyRealizedGrossPL = 'DailyRealizedGrossPL'
    VenueAccountName = 'VenueAccountName'
    TradeEntryRequestBlock = 'TradeEntryRequestBlock'
    LastMkt = 'LastMkt'
    BuyAvgPx = 'BuyAvgPx'
    SellAvgPx = 'SellAvgPx'
    TransferredInAmt = 'TransferredInAmt'
    TransferredOutAmt = 'TransferredOutAmt'
    SecurityAccountPLBlock = 'SecurityAccountPLBlock'
    TodayRealizedPL = 'TodayRealizedPL'
    PositionTransferReportBlock = 'PositionTransferReportBlock'
    PositionTransferID = 'PositionTransferID'
    TransferStatus = 'TransferStatus'
    QtyToTransfer = 'QtyToTransfer'
    TransferTransType = 'TransferTransType'
    BackOfficeNotes = 'BackOfficeNotes'
    LastCapacity = 'LastCapacity'
    ExecOrigin = 'ExecOrigin'
    PartiesList = 'PartiesList'
    PartiesBlock = 'PartiesBlock'
    AllocFreeAccountID = 'AllocFreeAccountID'
    AllocSettlCurrency = 'AllocSettlCurrency'
    RouteList = 'RouteList'
    VenueAccount = 'VenueAccount'
    VenueActGrpName = 'VenueActGrpName'
    LastVenueOrdID = 'LastVenueOrdID'
    VenueExecID = 'VenueExecID'
    RouteBlock = 'RouteBlock'
    """List Wave"""
    OrderListWaveNotificationBlock = 'OrderListWaveNotificationBlock'
    OrderNotificationElements = "OrdNotificationElements"
    OrderListWaveStatus = 'OrderListWaveStatus'
    PercentQtyToRelease = 'PercentQtyToRelease'
    QtyPercentageProfile = 'QtyPercentageProfile'
    RootParentOrdID = 'RootParentOrdID'
    RouteID = 'RouteID'
    """Bag Wave"""
    QtyToRelease = 'QtyToRelease'
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
    LastPx = 'LastPx'
    LastTradedQty = 'LastTradedQty'
    SingleAllocClientAccountID = 'SingleAllocClientAccountID'
    AllocClientAccountID = 'AllocClientAccountID'
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
    ExecAllocList = 'ExecAllocList'
    ExecAllocBlock = 'ExecAllocBlock'
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
    TradeDate = 'TradeDate'
    Side = 'Side'
    AllocationInstructionQtyList = 'AllocationInstructionQtyList'
    AllocationInstructionQtyBlock = 'AllocationInstructionQtyBlock'
    BookingQty = 'BookingQty'
    WashBookAccountID = 'WashBookAccountID'
    SettlType = 'SettlType'
    PriceDelta = 'PriceDelta'
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
    SourceAccountID = 'SourceAccountID'
    Currency = "Currency"
    FreeNotes = 'FreeNotes'
    Price = 'Price'
    VenueClientAccountName = 'VenueClientAccountName'
    PostTradeExecStatus = 'PostTradeExecStatus'
    DiscloseExec = 'DiscloseExec'
    DayAvgPrice = 'DayAvgPrice'
    SuspendedCare = "SuspendedCare"
    ManualOrderCrossReplyBlock = 'ManualOrderCrossReplyBlock'
    ExecQty = 'ExecQty'
    OrderListWaveID = 'OrderListWaveID'
    SubCounterpartList = "SubCounterpartList"
    OrdIDList = "OrdIDList"
    OrdIDBlock = "OrdIDBlock"
    CustOrderHandlingInst = "CustOrderHandlingInst"

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
    Smallest_to_Biggest = "GSB"
    Biggest_to_Smallest = "GBS"
    Last_to_First = "GLF"
    First_to_Last = "GFL"
    Equal = 'GEQ'


class TimeInForces(Enum):
    DAY = 'DAY'
    GTD = 'GTD'
    ATC = 'ATC'
    GTC = 'GTC'


class OrdTypes(Enum):
    Limit = 'LMT'
    Market = 'MKT'
    StopLimit = 'STL'
    StopLimit_FULL = 'StopLimit'
    Limit_FULL = 'Limit'
    Funari = 'FUN'


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
    OrderWaveStatus_NEW = 'NEW'
    OrderBagStatus_TER = 'TER'


class CDResponsesConst(Enum):
    CDRequestType_MOD = 'MOD'
    CDRequestType_CAN = 'CAN'


# enums for Position

class SubscriptionRequestTypes(Enum):
    SubscriptionRequestType_SUB = 'SUB'
    SubscriptionRequestType_UNS = 'UNS'


class PosReqTypes(Enum):
    PosReqType_POS = 'POS'


class PositionTransferReportConst(Enum):
    TransferTransType_NEW = 'NEW'


class PositionValidities(Enum):
    PosValidity_ITD = 'ITD'
    PosValidity_DEL = 'DEL'
    PosValidity_TP1 = 'TP1'
    PosValidity_TP2 = 'TP2'
    PosValidity_TP3 = 'TP3'
    PosValidity_TP4 = 'TP4'
    PosValidity_TP5 = 'TP5'
    PosValidity_TP6 = 'TP6'
    PosValidity_TP7 = 'TP7'


class CrossAnnouncementReplyConst(Enum):
    CrossAnnouncementStatus_ACK = 'ACK'
    CrossAnnouncementStatus_NEW = 'NEW'
