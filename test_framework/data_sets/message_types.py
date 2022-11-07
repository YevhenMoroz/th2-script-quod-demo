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
    NewOrderList = 'Order_NewOrderList'
    NewOrderListReply = 'Order_NewOrderListReply'
    OrdListNotification = 'Order_OrdListNotification'
    OrderListWaveNotification = 'Order_OrderListWaveNotification'
    PositionReport = 'Order_PositionReport'
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
    AddOrdersToOrderListRequest = 'Order_AddOrdersToOrderListRequest'
    PositionTransferInstruction = 'Order_PositionTransferInstruction'
    PositionTransferReport = 'Order_PositionTransferReport'
    ComputeBookingFeesCommissionsRequest = 'Order_ComputeBookingFeesCommissionsRequest'
    ComputeBookingFeesCommissionsReply = 'Order_ComputeBookingFeesCommissionsReply'
    QuoteRequestActionRequest = "Order_QuoteRequestActionRequest"
    QuoteRequest = "Fix_QuoteRequest"
    QuoteRequestNotif = "Order_QuoteRequestNotif"
    QuoteRequestActionReply = "Order_QuoteRequestActionReply"
    BookingCancelReply = "Order_BookingCancelReply"


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


class QSMessageType(Enum):
    QuoteAdjustmentRequest = "Order_QuoteAdjustmentRequest"
    QuoteManualSettingsRequest = "Order_QuoteManualSettingsRequest"
    Quote = "Order_Quote"


class ReadLogMessageType(Enum):
    Csv_Message = "Csv_Message"


class CSMessageType(Enum):
    CDOrdAckBatchRequest = "Order_CDOrdAckBatchRequest"
    CDOrdNotif = "Order_CDOrdNotif"
