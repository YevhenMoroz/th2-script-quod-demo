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


class ORSMessageType(Enum):
    OrderSubmit = 'Order_OrderSubmit'
    TradeEntryRequest = 'Order_TradeEntryRequest'
    OrderListWaveCreationRequest = 'Order_OrderListWaveCreationRequest'
    UnMatchRequest = 'Order_UnMatchRequest'
    ManualOrderCrossRequest = 'Order_ManualOrderCrossRequest'
    OrderModificationRequest = 'Order_OrderModificationRequest'
    OrderBagModificationRequest = 'Order_OrderBagModificationRequest'
    OrderCancelRequest = 'Order_OrderCancelRequest'
