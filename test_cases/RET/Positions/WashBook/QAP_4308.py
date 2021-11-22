import logging
import os

from datetime import datetime
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from win_gui_modules.order_ticket import OrderTicketDetails
from test_cases.wrapper.ret_wrappers import get_order_id, verifier, accept_order, extract_parent_order_details, \
    get_wash_book_positions_details, split_limit_order, complete_order, decorator_try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4308"

    # region Declarations
    seconds, nanos = timestamps()  # Store case start time

    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    wash_book_service = Stubs.act_wash_book_positions
    qty = "100"
    price = "2"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    wash_book_account_care = "CareWB"
    wash_book_account_dma = "DMA Washbook"
    lookup = "TCS"
    recipient = "RIN-DESK (CL)"
    partial_desk = False
    disclose_flag = DiscloseFlagEnum.DEFAULT_VALUE
    # end region

    # region Extract values with Wash Book Position before order creation
    cum_sell_qty_care = get_wash_book_positions_details(security_account=wash_book_account_care,
                                                        column_name="CumSellQty",
                                                        act=wash_book_service,
                                                        base_request=base_request)

    cum_buy_qty_dma = get_wash_book_positions_details(security_account=wash_book_account_dma,
                                                      column_name="CumBuyQty",
                                                      act=wash_book_service,
                                                      base_request=base_request)
    # end region

    # region create Care order via FE step 1
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    order_ticket.set_limit(price)
    order_ticket.set_washbook(wash_book_account_care)
    order_ticket.set_care_order(recipient, partial_desk, disclose_flag)
    order_ticket.sell()

    order_details = NewOrderDetails()
    order_details.set_lookup_instr(lookup)
    order_details.set_default_params(base_request)
    order_details.set_order_details(order_ticket)

    call(order_ticket_service.placeOrder, order_details.build())
    # end region

    care_order_id = get_order_id(base_request)

    accept_order(lookup, qty, price)

    # region step 2
    split_limit_order(base_request, qty, order_type)
    # end region

    call(order_book_service.closeWindow, base_request)

    # region

    # region Verify step 3
    cum_sell_qty = get_wash_book_positions_details(security_account=wash_book_account_care,
                                                   column_name="CumSellQty",
                                                   act=wash_book_service,
                                                   base_request=base_request)
    verifier(case_id=case_id,
             event_name="CumSellQty After created Care order",
             expected_value=cum_sell_qty_care,
             actual_value=cum_sell_qty)
    # end region

    # region create Market order via FE step 5
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    order_ticket.set_limit(price)
    order_ticket.set_washbook(wash_book_account_dma)
    order_ticket.buy()

    order_details = NewOrderDetails()
    order_details.set_lookup_instr(lookup)
    order_details.set_default_params(base_request)
    order_details.set_order_details(order_ticket)

    call(order_ticket_service.placeOrder, order_details.build())

    dma_order_id = get_order_id(base_request)
    # end region

    # region Verify order statuses step 5
    care_order_status = extract_parent_order_details(base_request, "ExecSts", wash_book_account_care, care_order_id)
    verifier(case_id=case_id,
             event_name="Care Order Status",
             expected_value="Filled",
             actual_value=care_order_status)

    dma_order_status = extract_parent_order_details(base_request, "ExecSts", wash_book_account_dma, dma_order_id)
    verifier(case_id=case_id,
             event_name="DMA Order Status",
             expected_value="Filled",
             actual_value=dma_order_status)
    # end region

    # region Extract and Verify Wash Book fields after filled orders steps 6 and 7
    cum_sell_qty_care_step6 = get_wash_book_positions_details(security_account=wash_book_account_care,
                                                              column_name="CumSellQty",
                                                              act=wash_book_service,
                                                              base_request=base_request)
    verifier(case_id=case_id,
             event_name="CumSellQty after filled Care order and DMA order",
             expected_value=str(int(cum_sell_qty_care) + 100),
             actual_value=cum_sell_qty_care_step6)

    cum_buy_qty_dma_step7 = get_wash_book_positions_details(security_account=wash_book_account_dma,
                                                            column_name="CumBuyQty",
                                                            act=wash_book_service,
                                                            base_request=base_request)
    verifier(case_id=case_id,
             event_name="CumBuyQty after filled Care order and DMA order",
             expected_value=str(int(cum_buy_qty_dma) + 100),
             actual_value=cum_buy_qty_dma_step7)
    # end region

    # region Complete order 8
    complete_order(base_request, care_order_id)
    # end region

    # region Extract and Verify ExecType filed step 8
    exec_type_care_order = extract_parent_order_details(base_request, "ExecType", wash_book_account_care, care_order_id)
    verifier(case_id=case_id,
             event_name="ExecutionType field after 'Complete' execution",
             expected_value="DoneForDay",
             actual_value=exec_type_care_order)
    # end region

    # region Book Care order step 9
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base_request)
    modify_request.set_filter(["Order ID", care_order_id])
    call(middle_office_service.bookOrder, modify_request.build())
    # end region

    # region Extract and Verify CumSellQty field for CareWB security account step 10
    cum_sell_qty_care_step10 = get_wash_book_positions_details(security_account=wash_book_account_care,
                                                               column_name="CumSellQty",
                                                               act=wash_book_service,
                                                               base_request=base_request)
    verifier(case_id=case_id,
             event_name="CumSellQty field  after 'Complete' and 'Book' Care order",
             expected_value=str(int(cum_sell_qty_care_step6) - 100),
             actual_value=cum_sell_qty_care_step10)
    # end region

    # region Book DMA order step 11
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base_request)
    modify_request.set_filter(["Order ID", dma_order_id])
    call(middle_office_service.bookOrder, modify_request.build())
    # end region

    # region Extract and Verify CumBuyQty
    cum_buy_qty_dma_step11 = get_wash_book_positions_details(security_account=wash_book_account_dma,
                                                             column_name="CumBuyQty",
                                                             act=wash_book_service,
                                                             base_request=base_request)
    verifier(case_id=case_id,
             event_name="CumBuyQty after 'Book' DMA order",
             expected_value=str(int(cum_buy_qty_dma_step7) - 100),
             actual_value=cum_buy_qty_dma_step11)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
