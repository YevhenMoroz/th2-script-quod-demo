# from th2_grpc_act_gui_quod.order_ticket_pb2 import OrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import AlgoOrderDetails
# from th2_grpc_act_gui_quod.order_ticket_pb2 import TWAPStrategyParams
# from th2_grpc_act_gui_quod.order_ticket_pb2 import QuodParticipationStrategyParams,
from th2_grpc_act_gui_quod import order_ticket_pb2, common_pb2, order_ticket_fx_pb2, ar_operations_pb2
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from .algo_strategies import TWAPStrategy, MultilistingStrategy, QuodParticipationStrategy
from .common_wrappers import CommissionsDetails, BaseTileDetails
from enum import Enum


class OrderTicketDetails:

    def __init__(self):
        self.order = order_ticket_pb2.OrderDetails()

    def set_client(self, client: str):
        self.order.client = client

    def set_instrument(self, instrument: str):
        self.order.instrument = instrument

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

    def build(self):
        return self.order


class OrderTicketValues(Enum):
    INSTRUMENT = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.INSTRUMENT
    PRICELARGE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.PRICELARGE
    PRICEPIPS = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.PRICEPIPS
    # ORDERTYPE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.ORDERTYPE
    QUANTITY = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.QUANTITY
    CLIENT = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.CLIENT
    TIMEINFORCE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.TIMEINFORCE
    SLIPPAGE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.SLIPPAGE
    STOPPRICE = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.STOPPRICE
    # DISPLAYQTY = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedType.DISPLAYQTY


class ExtractFxOrderTicketValuesRequest:

    def __init__(self, data: BaseTileDetails, extractionId: str = 'extractFXOrderTicketValues'):
        self.request = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest()
        self.request.data.CopyFrom(data)
        self.request.extractionId = extractionId

    def get_instrument(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.INSTRUMENT)

    def get_price_large(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.PRICELARGE)

    def get_price_pips(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.PRICEPIPS)

    def get_order_type(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.ORDERTYPE)

    def get_quantity(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.QUANTITY)

    def get_display_quantity(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.DISPLAYQTY)

    def get_client(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.CLIENT)

    def get_tif(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.TIMEINFORCE)

    def get_slippage(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.SLIPPAGE)

    def get_stop_price(self, unic_id: str):
        self.get_extract_value(unic_id, OrderTicketValues.STOPPRICE)

    def get_extract_value(self, name: str, field: OrderTicketValues):
        extracted_value = order_ticket_fx_pb2.ExtractFxOrderTicketValuesRequest.ExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = name
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


class OrderTicketExtractedValue(Enum):
    DISCLOSE_FLAG = order_ticket_pb2.ExtractOrderTicketValuesRequest.OrderTicketExtractedType.DISCLOSE_FLAG
    ERROR_MESSAGE = order_ticket_pb2.ExtractOrderTicketValuesRequest.OrderTicketExtractedType.ERROR_MESSAGE


class ExtractOrderTicketValuesRequest:

    def __init__(self, base_request, extractionId: str = 'extractOrderTicketValues'):
        self.request = order_ticket_pb2.ExtractOrderTicketValuesRequest()
        self.request.base.CopyFrom(base_request)
        self.request.extractionId = extractionId

    def get_disclose_flag_state(self):
        self.get_extract_value(OrderTicketExtractedValue.DISCLOSE_FLAG)

    def get_extract_value(self, field: OrderTicketExtractedValue):
        extracted_value = order_ticket_pb2.ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = "Disclose flag state extraction"
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request


class ExtractOrderTicketErrorsRequest:

    def __init__(self, base_request, extractionId: str = 'ErrorMessageExtractionID'):
        self.request = order_ticket_pb2.ExtractOrderTicketValuesRequest()
        self.request.base.CopyFrom(base_request)
        self.request.extractionId = extractionId

    def extract_error_message(self):
        self.get_extract_value(OrderTicketExtractedValue.ERROR_MESSAGE)

    def get_extract_value(self, field: OrderTicketExtractedValue):
        extracted_value = order_ticket_pb2.ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
        extracted_value.type = field.value
        extracted_value.name = "ErrorMessage"
        self.request.extractedValues.append(extracted_value)

    def build(self):
        return self.request

