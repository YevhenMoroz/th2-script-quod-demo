import logging
import time
from datetime import datetime
from th2_grpc_hand import rhbatch_pb2

import quod_qa.wrapper.eq_fix_wrappers
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1047"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    qty_percent = "100"
    price = "30"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    handl_ins = 3  # Care
    order_type = 2  # Limit
    side = 1  # Buy
    tif = 0  # Day

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region create CO
    quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, handl_ins, side, client, order_type, qty, tif, price)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    # endregion

    # region Direct order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))

        eq_wrappers.direct_order(lookup, price, qty, qty_percent)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    # endregion
    # region check sub Order status
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_sts = ExtractionDetail("lvl_1.sts", "Sts")
    child1_qty = ExtractionDetail("lvl_1.qty", "Qty")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_sts,child1_qty])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking child order")
    verifier.compare_values("Sts", "Open", request["lvl_1.sts"])
    verifier.compare_values("Qty", qty, request["lvl_1.qty"])
    verifier.verify()
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
