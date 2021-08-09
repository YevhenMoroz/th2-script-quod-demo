import logging

from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

def execute(report_id, session_id):
    case_name = "QAP-3875"
    # region Declarations
    qty = "900"
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
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region create 1 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id1 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region create 2 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id2 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region create 3 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id3 = eq_wrappers.get_order_id(base_request)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
   
    # region DirectChildCare these orders
    eq_wrappers.direct_child_care_order('100', 'ChiX direct access', recipient=Stubs.custom_config['qf_trading_fe_user']
                                        , count=3)
    # endregion

    order_id1 = eq_wrappers.get_order_id(base_request)
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[order_id1])
    child1_id = ExtractionDetail("child_ord_sts", "Sts")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking child_ord_id")
    verifier.compare_values("Status", "Open", request["child_ord_sts"])
    verifier.verify()
