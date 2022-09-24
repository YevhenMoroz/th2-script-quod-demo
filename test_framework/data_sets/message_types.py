from enum import Enum


class FIXMessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    ExecutionReport = "ExecutionReport"
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
    OrderBagModificationRequest = 'Order_OrderBagModificationRequest'
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

class ReadLogMessageType(Enum):
    Csv_Message = "Csv_Message"

class CSMessageType(Enum):
    CDOrdAckBatchRequest = "Order_CDOrdAckBatchRequest"
    CDOrdNotif = "Order_CDOrdNotif"
