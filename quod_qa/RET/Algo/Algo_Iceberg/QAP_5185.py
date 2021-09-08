import logging
import os

from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verify_ent, verification
from quod_qa.wrapper.ret_wrappers import verifier, extract_parent_order_details

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order(base_request, client, order_type, price, tif, lookup, qty, side, display_qty=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    if display_qty:
        order_ticket.set_display_qty(display_qty)
    if side == 'Buy':
        order_ticket.buy()
    elif side == 'Sell':
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket

    call(order_ticket_service.placeOrder, new_order_details.build())


def execute(session_id, report_id):
    case_name = "QAP_5175"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    client = "HAKKIM"
    qty = "1000"
    price = "10"
    order_type = "Limit"
    tif = "Day"
    lookup = "T55FD"
    parent_order_details_id = 'ParentOrderDetails'
    child_order_details_id_lvl1 = "ChildOrderDetailsLvl1"
    # endregion

    common_act = Stubs.win_act
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # end region

    # region Create order Pre-condition
    create_order(base_request, client, order_type, price, tif, lookup, qty, side='Sell')
    # end region

    # region Create Iceberg algo order step 1
    create_order(base_request, client, order_type, price, tif, lookup, qty, side='Buy', display_qty='500')
    # end region

    # region Extract and Verify parent order details
    order_status = extract_parent_order_details(base_request, column_name='ExecSts',
                                                extraction_id=parent_order_details_id)
    verifier(case_id, event_name='Check order parent Status', expected_value='Filled',
             actual_value=order_status)

    order_display_qty = extract_parent_order_details(base_request, column_name='DisplQty',
                                                     extraction_id=parent_order_details_id)
    verifier(case_id, event_name='Check order parent Display Qty', expected_value='500', actual_value=order_display_qty)
    # end region

    child_order_info_extraction = child_order_details_id_lvl1
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(child_order_info_extraction)

    child_lvl_1_1_order_qty = ExtractionDetail('First child order Qty', 'Qty')
    child_lvl_1_1_order_execsts = ExtractionDetail('First child order Execution Status', 'ExecSts')
    child_lvl_1_1_order_exepcy = ExtractionDetail('First child order Execution Policy', 'ExecPcy')

    sub_lvl_1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child_lvl_1_1_order_qty,
                                                                                           child_lvl_1_1_order_execsts,
                                                                                           child_lvl_1_1_order_exepcy])
    sub_lvl1_1_info = OrderInfo.create(actions=[sub_lvl_1_1_ext_action])

    child_lvl_1_2_order_qty = ExtractionDetail('Second child order Qty', 'Qty')
    child_lvl_1_2_order_execsts = ExtractionDetail('Second child order Execution Status', 'ExecSts')
    child_lvl_1_2_order_execpcy = ExtractionDetail('Second child order Execution Policy', 'ExecPcy')

    sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child_lvl_1_2_order_qty,
                                                                                          child_lvl_1_2_order_execsts,
                                                                                          child_lvl_1_2_order_execpcy])
    sub_lvl1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

    sub_orders_details = OrdersDetails.create(order_info_list=[sub_lvl1_1_info,
                                                               sub_lvl1_2_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_orders_details))

    call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())

    call(common_act.verifyEntities, verification(child_order_info_extraction, 'Check First Child order details',
                                                 [verify_ent('Child order Qty', child_lvl_1_1_order_qty.name, '500'),
                                                  verify_ent('Child order Exec Status',
                                                             child_lvl_1_1_order_execsts.name,
                                                             'Filled'),
                                                  verify_ent('Child order Exec Policy', child_lvl_1_1_order_exepcy.name,
                                                             'DMA')]))

    call(common_act.verifyEntities, verification(child_order_info_extraction, 'Check Second Child order details',
                                                 [verify_ent('Child order Qty', child_lvl_1_2_order_qty.name, '500'),
                                                  verify_ent('Child order Exec Status',
                                                             child_lvl_1_2_order_execsts.name, 'Filled'),
                                                  verify_ent('Child order Exec Policy',
                                                             child_lvl_1_2_order_execpcy.name, 'DMA')]))

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")