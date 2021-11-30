import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3875"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "40"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create 1 CO order
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id1 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region create 2 CO order
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id2 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region create 3 CO order
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id3 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion

    # region DirectChildCare these orders
    eq_wrappers.direct_child_care_order('100', 'ChiX direct access', recipient='vskulinec', count=3)
    # endregion

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_details.set_filter(['Order ID', order_id1])
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("Sts1", "Sts")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))

    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Sts', 'Open', request['Sts1'])
    verifier.verify()

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_details.set_filter(['Order ID', order_id2])
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("Sts1", "Sts")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Sts', 'Open', request['Sts1'])
    verifier.verify()

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_details.set_filter(['Order ID', order_id3])
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("Sts1", "Sts")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))

    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Sts', 'Open', request['Sts1'])
    verifier.verify()
