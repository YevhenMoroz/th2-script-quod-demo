from custom.basic_custom_actions import create_store_event_request
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.order_book_pb2_grpc import OrderBookServiceStub
from grpc_modules.win_act_pb2_grpc import HandWinActStub
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.utils import call, get_base_request, prepare_fe, set_session_id, close_fe
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, ExtractionInfo, OrdersDetails, ExtractionDetail
from grpc_modules import order_ticket_pb2_grpc, order_book_pb2_grpc, win_act_pb2_grpc
from channels import Channels
# from win_gui_modules.base_test import BaseTest
from win_gui_modules.wrappers import *
# from configuration import qf_trading_fe_user
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
# from grpc_modules.verifier_pb2_grpc import VerifierStub
# from grpc_modules.verifier_pb2 import CheckpointRequest
import time


# class QAP_1641(BaseTest):
#
# def __init__(self, channels: Channels, parent_event):
#     super().__init__(channels)
#     self.create_test_event(parent_event, "QAP-1641", "[TWAP] Check implement of MaxParticipation for TWAP")
#
# def create_checkpoint(self):
#     verifier = VerifierStub(self.Channels.verifier_channel)
#     request = CheckpointRequest(description="TestCheckpoint", parent_event_id=self._event_id)
#     return verifier.createCheckpoint(request).checkpoint
#
# def execute(self):

def execute(report_id, session_id):
    global sor_order_params, pending_er_params, new_er_params
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    # act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    sim = Stubs.sim

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-1641 [TWAP] Check implement of MaxParticipation for TWAP"
    case_id = bca.create_event(case_name, report_id)
    # case_id = create_event_id()
    event_store.StoreEvent(request=create_store_event_request(case_name, case_id, report_id))
    set_base(session_id, case_id)

    # common_act = HandWinActStub(Channels.ui_act_channel)
    #
    # act2 = OrderBookServiceStub(Channels.ui_act_channel)
    #
    order_info_extraction = "getOrderInfo"
    qty = "8000"
    limit = "1.2"
    lookup = "ACT"

    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(limit)
    order_ticket.set_client("CLIENT1")
    order_ticket.set_order_type("Limit")
    order_ticket.set_care_order("HD4", True)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(get_base_request(session_id, case_id))

    # call = self.call
    #
    # set_base(self._session_id, self._event_id)
    #
    act = order_ticket_pb2_grpc.OrderTicketServiceStub(Channels.ui_act_channel)
    act2 = order_book_pb2_grpc.OrderBookServiceStub(Channels.ui_act_channel)
    common_act = win_act_pb2_grpc.HandWinActStub(Channels.ui_act_channel)

    call(act.placeOrder, new_order_details.build())

    order_ticket = OrderTicketDetails()
    twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
    twap_strategy.set_start_date("Now")
    twap_strategy.set_end_date("Now", "0.5")
    twap_strategy.set_waves("4")
    twap_strategy.set_max_participation("25")
    twap_strategy.set_aggressivity("Aggressive")

    order_info_extraction = "getOrderInfo"

    call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
    call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                 [verify_ent("Order Status", "order.status", "Open")]))

    modify_order_details = ModifyOrderDetails()
    modify_order_details.set_default_params(get_base_request(session_id, case_id))
    modify_order_details.set_order_details(order_ticket)

    call(act2.splitOrder, modify_order_details.build())

    # step 4 make trade 10000

    order_ticket_dma1 = OrderTicketDetails()
    order_ticket_dma1.set_quantity('10000')
    order_ticket_dma1.set_limit('1.2')
    order_ticket_dma1.buy()

    act_dma1 = order_ticket_pb2_grpc.OrderTicketServiceStub(Channels.ui_act_channel)

    dma_order_details = NewOrderDetails()
    dma_order_details.set_lookup_instr(lookup)
    dma_order_details.set_order_details(order_ticket_dma1)
    dma_order_details.set_default_params(get_base_request(session_id, case_id))

    call(act_dma1.placeOrder, dma_order_details.build())

    order_ticket_dma2 = OrderTicketDetails()
    order_ticket_dma2.set_quantity('10000')
    order_ticket_dma2.set_limit('1.2')
    order_ticket_dma2.sell()

    act_dma2 = order_ticket_pb2_grpc.OrderTicketServiceStub(Channels.ui_act_channel)

    dma_order_details = NewOrderDetails()
    dma_order_details.set_lookup_instr(lookup)
    dma_order_details.set_order_details(order_ticket_dma2)
    dma_order_details.set_default_params(get_base_request(session_id, case_id))

    call(act_dma2.placeOrder, dma_order_details.build())

    time.sleep(120)

    #  make trade 5000

    order_ticket_dma1 = OrderTicketDetails()
    order_ticket_dma1.set_quantity('5000')
    order_ticket_dma1.set_limit('1.2')
    order_ticket_dma1.buy()

    act_dma1 = order_ticket_pb2_grpc.OrderTicketServiceStub(Channels.ui_act_channel)

    dma_order_details = NewOrderDetails()
    dma_order_details.set_lookup_instr(lookup)
    dma_order_details.set_order_details(order_ticket_dma1)
    dma_order_details.set_default_params(get_base_request(session_id, case_id))

    call(act_dma1.placeOrder, dma_order_details.build())

    order_ticket_dma2 = OrderTicketDetails()
    order_ticket_dma2.set_quantity('5000')
    order_ticket_dma2.set_limit('1.2')
    order_ticket_dma2.sell()

    act_dma2 = order_ticket_pb2_grpc.OrderTicketServiceStub(Channels.ui_act_channel)

    dma_order_details = NewOrderDetails()
    dma_order_details.set_lookup_instr(lookup)
    dma_order_details.set_order_details(order_ticket_dma2)
    dma_order_details.set_default_params(get_base_request(session_id, case_id))

    call(act_dma2.placeOrder, dma_order_details.build())

    time.sleep(30)

    # check child orders

    extraction_id = "order.care"

    sub_lv2_1_qty = ExtractionDetail("subOrder_1_lv2.qty", "Qty")
    sub_lv2_2_qty = ExtractionDetail("subOrder_2_lv2.qty", "Qty")
    sub_lv2_3_qty = ExtractionDetail("subOrder_3_lv2.qty", "Qty")

    sub_lv2_details = OrdersDetails()
    sub_lv2_details.add_single_extraction_info(ExtractionInfo.create(detail=sub_lv2_1_qty))
    sub_lv2_details.add_single_extraction_info(ExtractionInfo.create(detail=sub_lv2_2_qty))
    sub_lv2_details.add_single_extraction_info(ExtractionInfo.create(detail=sub_lv2_3_qty))
    length_name = "subOrders_lv2.length"
    sub_lv2_details.extract_length(length_name)

    sub_lv1_info = ExtractionInfo()
    sub_lv1_qty = ExtractionDetail("subOrder_lv1.qty", "Qty")
    sub_lv1_info.add_order_details(sub_lv1_qty)
    sub_lv1_info.set_sub_orders_details(sub_lv2_details)

    main_order_info = ExtractionInfo.create(sub_order_details=OrdersDetails.create(info=sub_lv1_info))

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(get_base_request(session_id, case_id))
    main_order_details.set_extraction_id(extraction_id)
    main_order_details.set_filter(["Lookup", "IMP", "ExecPcy", "Care"])
    main_order_details.add_single_extraction_info(main_order_info)

    call(act2.getOrdersDetails, main_order_details.request())

    call(common_act.verifyEntities, verification(extraction_id, "Checking child orders",
                                                 [verify_ent("Sub Lvl 1 Qty", sub_lv1_qty.name, "8,000"),
                                                  verify_ent("Sub 1 Lvl 2 Qty", sub_lv2_1_qty.name, "1,666"),
                                                  verify_ent("Sub 2 Lvl 2 Qty", sub_lv2_2_qty.name, "1,333"),
                                                  verify_ent("Sub 3 Lvl 2 Qty", sub_lv2_3_qty.name, "2,000"),
                                                  verify_ent("Sub order Lvl 2 count", length_name, "3")]))
