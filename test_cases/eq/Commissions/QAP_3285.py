import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier, VerificationMethod
from test_framework.old_wrappers import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3285"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    lookup = "VETO"
    client = "CLIENT_COMM_1"
    account = "CLIENT_COMM_1_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)

    no_allocs = [
        {
            'AllocAccount': account,
            'AllocQty': qty
        }
    ]

    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            float(price), int(qty), 1)

        test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price, no_allocs)
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
    child1_id = ExtractionDetail("lvl_1.cl_comm", "Client Commission")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Client Commission")
    print(request["lvl_1.cl_comm"])
    verifier.compare_values("Client Commission", int(int(qty) * 0.01),request["lvl_1.cl_comm"],
                            VerificationMethod.CONTAINS)
    verifier.compare_values("Client Commission","9", request["lvl_1.cl_comm"],
                            VerificationMethod.CONTAINS)
    verifier.verify()
    # endregion
