# from th2_grpc_act_gui_quod.order_ticket_pb2 import OrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import AlgoOrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import TWAPStrategyParams
# from th2_grpc_act_gui_quod.order_ticket_pb2 import QuodParticipationStrategyParams,
from th2_grpc_act_gui_quod import order_ticket_pb2, common_pb2

#from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from th2_grpc_act_gui_quod import order_ticket_pb2, common_pb2, order_ticket_fx_pb2
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from .algo_strategies import TWAPStrategy, MultilistingStrategy, QuodParticipationStrategy
from .common_wrappers import CommissionsDetails
from enum import Enum


class OrderTicketDetails:

    def __init__(self):
        self.order = order_ticket_pb2.OrderDetails()

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

    def set_tif(self, tif: str):
        self.order.timeInForce = tif

    def set_account(self, account: str):
         self.order.account = account

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

    def add_multilisting_strategy(self, strategy_type: str) -> MultilistingStrategy:
        self.order.algoOrderParams.CopyFrom(order_ticket_pb2.AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.multilistingStrategy.CopyFrom(order_ticket_pb2.MultilistingStrategy())
        return MultilistingStrategy(self.order.algoOrderParams.multilistingStrategy)

    def add_quod_participation_strategy(self, strategy_type: str) -> QuodParticipationStrategy:
        self.order.algoOrderParams.CopyFrom(order_ticket_pb2.AlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.quodParticipationStrategyParams.CopyFrom(
            order_ticket_pb2.QuodParticipationStrategyParams())
        return QuodParticipationStrategy(self.order.algoOrderParams.quodParticipationStrategyParams)

    def set_care_order(self, desk: str, partial_desk: bool = False,
                       disclose_flag: DiscloseFlagEnum = DiscloseFlagEnum.DEFAULT_VALUE):
        self.order.careOrderParams.desk = desk
        self.order.careOrderParams.partialDesk = partial_desk
        self.order.careOrderParams.discloseFlag = disclose_flag

    def set_washbook(self, washbook: str):
        self.order.advOrdParams.washbook = washbook

    def add_commissions_details(self) -> CommissionsDetails:
        self.order.commissionsParams.CopyFrom(common_pb2.CommissionsDetails())
        return CommissionsDetails(self.order.commissionsParams)

    def build(self):
        return self.order


class FXOrderDetails:

    def __init__(self):
        self.order = order_ticket_fx_pb2.FxOrderDetails()

    def set_price_large(self, priceLarge: str):
        self.order.priceLarge = priceLarge

    def set_price_pips(self, pricePips: str):
        self.order.pricePips = pricePips

    def set_limit(self, limit: str):
        self.order.limit = limit

    def set_qty(self, qty: str):
        self.order.qty = qty

    def set_client(self, client: str):
        self.order.client = client

    def set_tif(self, timeInForce: str):
        self.order.timeInForce = timeInForce

    def set_slippage(self, slippage: str):
        self.order.slippage = slippage

    def set_stop_price(self, stopPrice: str):
        self.order.stopPrice = stopPrice

    def set_order_type(self, order_type: str):
        self.order.orderType = order_type

    def build(self):
        return self.order


