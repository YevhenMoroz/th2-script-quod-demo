# from th2_grpc_act_gui_quod.order_ticket_pb2 import OrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import AlgoOrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import TWAPStrategyParams
# from th2_grpc_act_gui_quod.order_ticket_pb2 import QuodParticipationStrategyParams,
from enum import Enum

from th2_grpc_act_gui_quod import order_ticket_pb2, common_pb2, order_ticket_fx_pb2
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from .algo_strategies import (TWAPStrategy, MultilistingStrategy, QuodParticipationStrategy, FXMultilistingStrategy,
                              FXTWAPStrategy)
from .common_wrappers import CommissionsDetails


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

    def set_expire_date(self, expire_date: str):
        self.order.expireDate = expire_date

    def set_order_type(self, order_type: str):
        self.order.orderType = order_type

    def set_tif(self, tif: str):
        self.order.timeInForce = tif

    def set_account(self, account: str):
        self.order.client = account

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
        self.order.isShouldBePlaced = False
        self.order.isShouldBeClosed = False

    def set_price_large(self, priceLarge: str):
        self.order.priceLarge = priceLarge

    def set_price_pips(self, pricePips: str):
        self.order.pricePips = pricePips

    def set_limit(self, limit: str):
        self.order.limit = limit

    def set_qty(self, qty: str):
        self.order.qty = qty

    def set_display_qty(self, qty: str):
        self.order.displayQty = qty

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

    def set_place(self, isShouldBePlaced: bool = True):
        self.order.isShouldBePlaced = isShouldBePlaced

    def set_close(self, isShouldBeClosed: bool = True):
        self.order.isShouldBeClosed = isShouldBeClosed

    def set_pending(self, isPending: bool = True):
        self.order.isPending = isPending

    def set_keep_open(self, isKeepOpen: bool = True):
        self.order.isKeepOpen = isKeepOpen

    def set_custom_algo_check_box(self, isCustomAlgo: bool = True):
        self.order.isCustomAlgo = isCustomAlgo

    def set_custom_algo(self, customAlgo: str):
        self.order.customAlgo = customAlgo

    def set_strategy(self, strategy: str):
        self.order.strategy = strategy

    def set_child_strategy(self, childStrategy: str):
        self.order.childStrategy = childStrategy

    def click_pips(self, click_pips: int):
        self.order.clickPips = click_pips

    def click_qty(self, click_qty: int):
        self.order.clickQty = click_qty

    def click_slippage(self, click_slippage: int):
        self.order.clickSlippage = click_slippage

    def click_stop_price(self, click_stop_price: int):
        self.order.clickStopPrice = click_stop_price

    def click_display_qty(self, click_display_qty: int):
        self.order.clickDisplayQty = click_display_qty

    def set_care_order(self, desk: str, partial_desk: bool = False,
                       disclose_flag: DiscloseFlagEnum = DiscloseFlagEnum.DEFAULT_VALUE):
        self.order.careOrderParams.desk = desk
        self.order.careOrderParams.partialDesk = partial_desk
        self.order.careOrderParams.discloseFlag = disclose_flag

    def add_multilisting_strategy(self, strategy_type: str) -> FXMultilistingStrategy:
        self.order.algoOrderParams.CopyFrom(order_ticket_fx_pb2.FXAlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.multilistingStrategy.CopyFrom(order_ticket_fx_pb2.FXMultilistingStrategy())
        return FXMultilistingStrategy(self.order.algoOrderParams.multilistingStrategy)

    def add_twap_strategy(self, strategy_type: str) -> FXTWAPStrategy:
        self.order.algoOrderParams.CopyFrom(order_ticket_fx_pb2.FXAlgoOrderDetails())
        self.order.algoOrderParams.strategyType = strategy_type
        self.order.algoOrderParams.twapStrategy.CopyFrom(order_ticket_fx_pb2.FXTWAPStrategyParams())
        return FXTWAPStrategy(self.order.algoOrderParams.twapStrategy)

    def build(self):
        return self.order


class OrderTicketValues(Enum):
    types = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType
    INSTRUMENT = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.INSTRUMENT
    PRICELARGE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.PRICELARGE
    PRICEPIPS = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.PRICEPIPS
    ORDERTYPE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.ORDERTYPE
    QUANTITY = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.QUANTITY
    CLIENT = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.CLIENT
    TIMEINFORCE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.TIMEINFORCE
    SLIPPAGE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.SLIPPAGE
    STOPPRICE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.STOPPRICE
    ALGO = types.ALGO
    STRATEGY = types.STRATEGY
    CHILD_STRATEGY = types.CHILD_STRATEGY
    IS_ALGO_CHECKED = types.IS_ALGO_CHECKED
    ERROR_MESSAGE_TEXT = types.ERROR_MESSAGE_TEXT
    BUY_SELL_BUTTON_TEXT = types.BUY_SELL_BUTTON_TEXT


class ExtractFxOrderTicketValuesRequest:

    def __init__(self, data: BaseTileData, extractionId: str = 'extractFXOrderTicketValues'):
        self.request = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest()
        self.request.data.CopyFrom(data)
        self.request.extractionId = extractionId

    def get_instrument(self, unic_id: str = 'fx_order_ticket.instrument'):
        self.get_extract_value(unic_id, OrderTicketValues.INSTRUMENT)

    def get_price_large(self, unic_id: str = 'fx_order_ticket.price_large'):
        self.get_extract_value(unic_id, OrderTicketValues.PRICELARGE)

    def get_price_pips(self, unic_id: str = 'fx_order_ticket.price_pips'):
        self.get_extract_value(unic_id, OrderTicketValues.PRICEPIPS)

    def get_order_type(self, unic_id: str = 'fx_order_ticket.order_type'):
        self.get_extract_value(unic_id, OrderTicketValues.ORDERTYPE)

    def get_quantity(self, unic_id: str = 'fx_order_ticket.quantity'):
        self.get_extract_value(unic_id, OrderTicketValues.QUANTITY)

    def get_client(self, unic_id: str = 'fx_order_ticket.client'):
        self.get_extract_value(unic_id, OrderTicketValues.CLIENT)

    def get_tif(self, unic_id: str = 'fx_order_ticket.tif'):
        self.get_extract_value(unic_id, OrderTicketValues.TIMEINFORCE)

    def get_slippage(self, unic_id: str = 'fx_order_ticket.slippage'):
        self.get_extract_value(unic_id, OrderTicketValues.SLIPPAGE)

    def get_stop_price(self, unic_id: str = 'fx_order_ticket.stop_price'):
        self.get_extract_value(unic_id, OrderTicketValues.STOPPRICE)

    def get_algo(self, algo: str = 'fx_order_ticket.algo'):
        self.get_extract_value(algo, OrderTicketValues.ALGO)

    def get_strategy(self, strategy: str = 'fx_order_ticket.strategy'):
        self.get_extract_value(strategy, OrderTicketValues.STRATEGY)

    def get_child_strategy(self, child_strategy: str = 'fx_order_ticket.child_strategy'):
        self.get_extract_value(child_strategy, OrderTicketValues.CHILD_STRATEGY)

    def get_is_algo_checked(self, is_algo_checked: str = 'fx_order_ticket.is_algo_checked'):
        self.get_extract_value(is_algo_checked, OrderTicketValues.IS_ALGO_CHECKED)

    def get_error_message_text(self, is_algo_checked: str = 'fx_order_ticket.error_message_text'):
        self.get_extract_value(is_algo_checked, OrderTicketValues.ERROR_MESSAGE_TEXT)

    def get_send_btn_text(self, is_algo_checked: str = 'fx_order_ticket.send_btn_text'):
        self.get_extract_value(is_algo_checked, OrderTicketValues.BUY_SELL_BUTTON_TEXT)

    def get_extract_value(self, name: str, field: OrderTicketValues):
        extracted_value = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request
