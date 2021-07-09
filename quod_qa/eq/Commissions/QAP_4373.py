import time

from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import get_base_request, call
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4373"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    lookup = "VETO"
    client = "CLIENT_FEES_1"
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_EUREX', "XEUR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_EUREX', 'XEUR',
                                                                      float(price), int(qty), 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price, insrument=instrument)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    eq_wrappers.accept_order(lookup, qty, price)
    eq_wrappers.manual_execution(base_request, qty, price)
    # region Verify
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("fees", "FeesAgent")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Fees")
    verifier.compare_values("FeeAgent", "10", request["fees"] )
    verifier.verify()
    # endregion


