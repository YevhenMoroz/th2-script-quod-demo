from enum import Enum


class FIXMessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
    ExternalExecutionReport = "ExternalExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"
    MarketDataRequest = "MarketDataRequest"
    QuoteRequestReject = "QuoteRequestReject"
    MarketDataIncrementalRefresh = "MarketDataIncrementalRefresh"
    MarketDataSnapshotFullRefresh = "MarketDataSnapshotFullRefresh"
    NewOrderList = "NewOrderList"
    ListStatus = "ListStatus"
    Confirmation = "Confirmation"
    AllocationInstruction = "AllocationInstruction"
    QuoteRequest = "QuoteRequest"
    NewOrderMultiLeg = "NewOrderMultileg"
    Quote = "Quote"
    MarketDataRequestReject = "MarketDataRequestReject"
    OrderCancelReject = "OrderCancelReject"
    QuoteCancel = "QuoteCancel"
    BusinessMessageReject = "BusinessMessageReject"
    Reject = 'Reject'
    Allocation = "Allocation"
    RequestForPositions = "RequestForPositions"


class ORSMessageType(Enum):
    OrderSubmit = 'Order_OrderSubmit'
    FixNewOrderSingle = 'Fix_NewOrderSingle'
    TradeEntryRequest = 'Order_TradeEntryRequest'
    OrderListWaveCreationRequest = 'Order_OrderListWaveCreationRequest'
    UnMatchRequest = 'Order_UnMatchRequest'
    ManualOrderCrossRequest = 'Order_ManualOrderCrossRequest'
    OrderModificationRequest = 'Order_OrderModificationRequest'
    OrderCancelRequest = 'Order_OrderCancelRequest'
    OrdReply = 'Order_OrdReply'
    OrdNotification = 'Order_OrdNotification'
    ExecutionReport = 'Order_ExecutionReport'
    DFDManagementBatch = 'Order_DFDManagementBatch'
    AllocationInstruction = 'Order_AllocationInstruction'
    OrdUpdate = 'Order_OrdUpdate'
    AllocationReport = 'Order_AllocationReport'
    Confirmation = 'Order_Confirmation'
    ConfirmationReport = 'Order_ConfirmationReport'
    ForceAllocInstructionStatusRequest = 'Order_ForceAllocInstructionStatusRequest'
    ForceAllocInstructionStatusReply = 'Order_ForceAllocInstructionStatusReply'
    CDNotifDealer = 'Order_CDNotifDealer'
    TradeEntryNotif = 'Order_TradeEntryNotif'
    BlockUnallocateRequest = 'Order_BlockUnallocateRequest'
    BookingCancelRequest = 'Order_BookingCancelRequest'
    ListCancelRequest = 'Order_ListCancelRequest'
    NewOrderList = 'Order_NewOrderList'
    NewOrderListReply = 'Order_NewOrderListReply'
    OrdListNotification = 'Order_OrdListNotification'
    OrderListWaveNotification = 'Order_OrderListWaveNotification'
    ManualOrderCrossReply = 'Order_ManualOrderCrossReply'
    OrderModificationReply = 'Order_OrderModificationReply'
    OrderBagCreationRequest = 'Order_OrderBagCreationRequest'
    OrderBagCreationReply = 'Order_OrderBagCreationReply'
    OrderBagNotification = 'Order_OrderBagNotification'
    OrderBagModificationRequest = 'Order_OrderBagModificationRequest'
    OrderBagModificationReply = 'Order_OrderBagModificationReply'
    OrderBagCancelRequest = 'Order_OrderBagCancelRequest'
    OrderBagCancelReply = 'Order_OrderBagCancelReply'
    OrderBagWaveRequest = 'Order_OrderBagWaveRequest'
    OrderBagWaveNotification = 'Order_OrderBagWaveNotification'
    OrderBagWaveModificationRequest = 'Order_OrderBagWaveModificationRequest'
    OrderBagWaveModificationReply = 'Order_OrderBagWaveModificationReply'
    OrderBagWaveCancelRequest = 'Order_OrderBagWaveCancelRequest'
    OrderBagWaveCancelReply = 'Order_OrderBagWaveCancelReply'
    OrderBagDissociateRequest = 'Order_OrderBagDissociateRequest'
    OrderBagDissociateReply = 'Order_OrderBagDissociateReply'
    AddOrdersToOrderListRequest = 'Order_AddOrdersToOrderListRequest'
    RemoveOrdersFromOrderListRequest = 'Order_RemoveOrdersFromOrderListRequest'
    OrderReply = 'Order_OrdReply'
    SuspendOrderManagementRequest = "Order_SuspendOrderManagementRequest"
    PositionTransferInstruction = 'Order_PositionTransferInstruction'
    PositionTransferCancelRequest = "Order_PositionTransferCancelRequest"
    PositionTransferCancelReply = "Order_PositionTransferCancelReply"
    PositionTransferReport = 'Order_PositionTransferReport'
    ComputeBookingFeesCommissionsRequest = 'Order_ComputeBookingFeesCommissionsRequest'
    ComputeBookingFeesCommissionsReply = 'Order_ComputeBookingFeesCommissionsReply'
    QuoteRequestActionRequest = "Order_QuoteRequestActionRequest"
    QuoteRequest = "Fix_QuoteRequest"
    QuoteRequestNotif = "Order_QuoteRequestNotif"
    QuoteRequestActionReply = "Order_QuoteRequestActionReply"
    BookingCancelReply = "Order_BookingCancelReply"
    BlockChangeConfirmationServiceRequest = 'Order_BlockChangeConfirmationServiceRequest'
    ForceAllocInstructionStatusBatchRequest = 'Order_ForceAllocInstructionStatusBatchRequest'
    BlockUnallocateBatchRequest = 'Order_BlockUnallocateBatchRequest'
    ForceAllocInstructionStatusBatchReply = 'Order_ForceAllocInstructionStatusBatchReply'
    BlockUnallocateBatchReply = 'Order_BlockUnallocateBatchReply'
    OrderUnMatchReply = 'Order_UnMatchReply'
    FixConfirmation = 'Fix_Confirmation'
    MassConfirmation = 'Order_MassConfirmation'
    NewOrderReply = 'Gateway_NewOrderReply'
    CheckOutOrderRequest = "Order_CheckOutOrderRequest"
    CheckOutOrderReply = "Order_CheckOutOrderReply"
    CheckInOrderRequest = 'Order_CheckInOrderRequest'
    CheckInOrderReply = 'Order_CheckInOrderReply'
    HeldOrderAckRequest = 'Order_HeldOrderAck'
    HeldOrderAckReply = 'Order_HeldOrderAckReply'
    MarkOrderRequest = 'Order_MarkOrderRequest'
    MarkOrderReply = 'Order_MarkOrderReply'
    DFDManagementBatchReply = 'Order_DFDManagementBatchReply'
    RemoveOrdersFromOrderListReply = 'Order_RemoveOrdersFromOrderListReply'
    ListCancelReply = 'Order_ListCancelReply'
    AddOrdersToOrderListReply = 'Order_AddOrdersToOrderListReply'
    OrderListWaveModificationRequest = 'Order_OrderListWaveModificationRequest'
    OrderListWaveModificationReply = 'Order_OrderListWaveModificationReply'
    OrderActionRequest = 'Order_OrderActionRequest'
    OrderActionReply = 'Order_OrderActionReply'
    TradeEntryBatchRequest = 'Order_TradeEntryBatchRequest'
    TradeEntryBatchReply = 'Order_TradeEntryBatchReply'
    SuspendOrderManagementReply = 'Order_SuspendOrderManagementReply'
    TradeEntryReply = "Order_TradeEntryReply"
    OrderSubmitReply = "Order_OrderSubmitReply"
    OrdRejectedNotif = 'Order_OrdRejectedNotif'
    FixOrderModificationRequest = "Fix_OrderModificationRequest"
    FixOrderCancelRequest = "Fix_OrderCancelRequest"
    OrderListWaveNotificationBlock = "OrderListWaveNotificationBlock"
    OrderListWaveCancelRequest = "Order_OrderListWaveCancelRequest"
    OrderListWaveCancelReply = 'Order_OrderListWaveCancelReply'
    NewOrderMultiLeg = "Order_NewOrderMultiLeg"
    FixNewOrderReply = "Fix_NewOrderReply"
    FixAllocationInstruction = 'Fix_AllocationInstruction'


class TradingRestApiMessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    NewOrderSingleReply = "NewOrderReply"
    OrderUpdate = "OrderUpdate"
    ExecutionReport = "ExecutionReport"
    NewOrderSingleSimulate = "NewOrderSingleSimulate"
    NewOrderSingleSimulateReply = "NewOrderSingleSimulateReply"
    OrderModificationRequest = "OrderModificationRequest"
    OrderModificationReply = "OrderModificationReply"
    OrderModificationReject = "OrderModificationReject"
    OrderCancelRequest = "OrderCancelRequest"
    OrderCancelReply = "OrderCancelReply"
    OrderCancelReject = "OrderCancelReject"
    MarketDataRequest = "MarketDataRequest"
    MarketDataReply = "MarketDataReply"
    MarketQuoteRequest = "MarketQuoteRequest"
    MarketQuoteReply = "MarketQuoteReply"
    MarketDataSnapshotFullRefresh = "MarketDataSnapshotFullRefresh"
    PositionRequest = "PositionRequest"
    PositionReply = "PositionReply"
    PositionReport = "PositionReport"
    OrderArchiveMassStatusRequest = 'OrderArchiveMassStatusRequest'
    OrderArchiveMassStatusRequestReply = 'OrderArchiveMassStatusRequestReply'
    VenueListRequest = "VenueListRequest"
    VenueListReply = "VenueListReply"
    HistoricalMarketDataRequest = 'HistoricalMarketDataRequest'
    HistoricalMarketDataReply = 'HistoricalMarketDataReply'


class ESMessageType(Enum):
    OrdReport = 'Gateway_OrdReport'
    ExecutionReport = 'Gateway_ExecutionReport'
    NewOrderReply = 'Gateway_NewOrderReply'
    OrderCancelReply = 'Gateway_OrderCancelReply'
    OrderModificationReply = "Gateway_OrderModificationReply"


class ResAPIMessageType(Enum):
    CreateVenue = "CreateVenue"
    ModifyVenue = "ModifyVenue"
    FindAllVenue = "FindAllVenue"
    CreateOrderVelocity = "CreateOrderVelocityLimit"
    FindAllOrderVelocity = "FindAllOrderVelocityLimit"
    DeleteOrderVelocity = "DeleteOrderVelocityLimit"
    ModifyOrderVelocity = "ModifyOrderVelocityLimit"


class PKSMessageType(Enum):
    RequestForPositions = "Order_RequestForPositions"
    RequestForFXPositions = "Order_RequestForFXPositions"
    FixRequestForPositions = "Fix_RequestForPositions"
    FixPositionReport = "Fix_PositionReport"
    FixPositionMaintenanceRequest = "Fix_PositionMaintenanceRequest"
    PositionReport = "Order_PositionReport"


class QSMessageType(Enum):
    QuoteAdjustmentRequest = "Order_QuoteAdjustmentRequest"
    QuoteManualSettingsRequest = "Order_QuoteManualSettingsRequest"
    Quote = "Order_Quote"


class ReadLogMessageType(Enum):
    Csv_Message = "Csv_Message"


class CSMessageType(Enum):
    CDOrdAckBatchRequest = "Order_CDOrdAckBatchRequest"
    CDOrdNotif = "Order_CDOrdNotif"
    ManualMatchExecToParentOrdersRequest = "Order_ManualMatchExecToParentOrdersRequest"
    ManualMatchExecToParentOrdersReply = "Order_ManualMatchExecToParentOrdersReply"
    ManualMatchExecsToParentOrderRequest = 'Order_ManualMatchExecsToParentOrderRequest'
    ManualMatchExecsToParentOrderReply = "Order_ManualMatchExecsToParentOrderReply"
    CDOrdAckBatchReply = "Order_CDOrdAckBatchReply"
    CDTransferRequest = "Order_CDTransferRequest"
    CDTransferReply = "Order_CDTransferReply"
    CDTransferNotif = 'Order_CDTransferNotif'
    CDTransferAck = 'Order_CDTransferAck'
    CDTransferAckReply = 'Order_CDTransferAckReply'
    CDOrdAssign = 'Order_CDOrdAssign'
    CDAssignReply = 'Order_CDAssignReply'
    UnMatchRequest = 'Internal_UnMatchRequest'


class MDAMessageType(Enum):
    MarketDataRequest = "Market_MarketDataRequest"
    MarketDataSnapshotFullRefresh = "Market_MarketDataSnapshotFullRefresh"


class AQSMessageType(Enum):
    FrontendQuery = 'Order_FrontendQuery'
    FrontendQueryReply = 'Order_FrontendQueryReply'


class StoredProcedureNamesForAqs(Enum):
    FEExecutionTransferList = 'FE_ExecutionTransfer_List'
    FE_OrdrFromOrdID_List = 'FE_OrdrFromOrdID_List'
