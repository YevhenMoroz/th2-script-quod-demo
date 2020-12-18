from grpc_modules import order_ticket_pb2
from .algo_strategies import TWAPStrategy


class OrderTicketDetails:

    def __init__(self):
        self.order = order_ticket_pb2.OrderDetails()

    def set_client(self, client: str):
        self.order.client = client

    def set_limit(self, limit: str):
        self.order.limit = limit

    def set_quantity(self, qty: str):
        self.order.qty = qty

    def set_order_type(self, order_type: str):
        self.order.orderType = order_type

    def buy(self):
        self.order.orderSide = order_ticket_pb2.OrderDetails.OrderSide.BUY

    def sell(self):
        self.order.orderSide = order_ticket_pb2.OrderDetails.OrderSide.SELL

    def submit(self):
        self.order.orderSide = order_ticket_pb2.OrderDetails.OrderSide.SUBMIT

    def set_care_order(self, desk: str, partial_desk: bool = False):
        self.order.careOrderParams.desk = desk
        self.order.careOrderParams.partialDesk = partial_desk

    def add_twap_strategy(self, strategy_type: str) -> TWAPStrategy:
        self.order.algoOrderParams.CopyFrom(order_ticket_pb2.AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.twapStrategy.CopyFrom(order_ticket_pb2.TWAPStrategyParams())
        return TWAPStrategy(self.order.algoOrderParams.twapStrategy)

    def build(self):
        return self.order
