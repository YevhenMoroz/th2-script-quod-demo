import logging
import time

import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-2998"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_FEES_1"
    account = "CLIENT_FEES_1_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    instrument ={
                'Symbol': 'IS0000000001_EUR',
                'SecurityID': 'IS0000000001',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XEUR'
            }
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_EUREX', "XEUR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_EUREX', 'XEUR',
            float(price), int(qty), 1)
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Verify
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("lvl_1.id", "Exec Fees")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Fees")
    verifier.compare_values("FeeAgent", "10", request["lvl_1.id"])
    verifier.verify()
    # endregion
    # endregion


