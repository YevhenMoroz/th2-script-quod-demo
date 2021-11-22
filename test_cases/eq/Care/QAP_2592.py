import logging
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from custom.verifier import Verifier
from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2592"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "800"
    price = "10"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE

    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregionA
    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id1 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion split order
    eq_wrappers.split_order(base_request, str(int(qty) + 100), 'Limit', price)
    # # endregion
    #
    # region check child DMA order
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("Qty", "Qty")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))

    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Qty', '800', request['Qty'])
    verifier.verify()

    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    # endregion split order
    eq_wrappers.accept_order('VETO', qty, price)

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())

    eq_wrappers.split_order(base_request, '0', 'Limit', price)
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
    print(result)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View",
                            'Quantity cannot be negative or null', result['ErrorMessage']
                            )
    verifier.verify()
