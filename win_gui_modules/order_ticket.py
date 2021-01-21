from th2_grpc_act_gui_quod.order_ticket_pb2 import OrderDetails
from th2_grpc_act_gui_quod.order_ticket_pb2 import AlgoOrderDetails
from th2_grpc_act_gui_quod.order_ticket_pb2 import TWAPStrategyParams
from th2_grpc_act_gui_quod.order_ticket_pb2 import QuodParticipationStrategyParams
from .algo_strategies import TWAPStrategy, MultilistingStrategy, QuodParticipationStrategy


class OrderTicketDetails:

    def __init__(self):
        self.order = OrderDetails()

    def set_client(self, client: str):
        self.order.client = client

    def set_limit(self, limit: str):
        self.order.limit = limit

    def set_stop_price(self, stop_price: str):
        self.order.stopPrice = stop_price

    def set_quantity(self, qty: str):
        self.order.qty = qty

    def set_order_type(self, order_type: str):
        self.order.orderType = order_type

    def buy(self):
        self.order.orderSide = OrderDetails.OrderSide.BUY

    def sell(self):
        self.order.orderSide = OrderDetails.OrderSide.SELL

    def submit(self):
        self.order.orderSide = OrderDetails.OrderSide.SUBMIT

    def set_care_order(self, desk: str, partial_desk: bool = False):
        self.order.careOrderParams.desk = desk
        self.order.careOrderParams.partialDesk = partial_desk

    def add_twap_strategy(self, strategy_type: str) -> TWAPStrategy:
        self.order.algoOrderParams.CopyFrom(AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.twapStrategy.CopyFrom(TWAPStrategyParams())
        return TWAPStrategy(self.order.algoOrderParams.twapStrategy)

    def add_multilisting_strategy(self, strategy_type: str) -> MultilistingStrategy:
        self.order.algoOrderParams.CopyFrom(AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.multilistingStrategy.CopyFrom(MultilistingStrategy())
        return MultilistingStrategy(self.order.algoOrderParams.multilistingStrategy)

    def add_quod_participation_strategy(self, strategy_type: str) -> QuodParticipationStrategy:
        self.order.algoOrderParams.CopyFrom(AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.quodParticipationStrategyParams.CopyFrom(
            QuodParticipationStrategyParams())
        return QuodParticipationStrategy(self.order.algoOrderParams.quodParticipationStrategyParams)

    def build(self):
        return self.order
