import logging
from datetime import datetime
from th2_grpc_hand import rhbatch_pb2
import time
#from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1717"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "3"
    client = "CLIENT1"
    lookup = "VETO"
    order_type = "Limit"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             'XPAR_CLIENT1', "XPAR", 3)

        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 3, 'CLIENT1', 2, qty, 6, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregions

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")
    order_id = ExtractionDetail("order_id", "Order ID")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_id,
                                                                                            order_qty,
                                                                                            order_price
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    request = call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")
                                                  ]))
    # endregion
    # region Direct
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             'XPAR_CLIENT1', "XPAR", 3)
        eq_wrappers.direct_order(lookup, qty, price, 100)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    # endregion
    order_id = eq_wrappers.get_order_id(base_request)
    # check Child Order status

    order_info_extraction = "getOrderInfo"
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(order_info_extraction)
    main_order_details.set_filter(["Order ID", eq_wrappers.get_order_id(base_request)])
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
    child_order_qty = ExtractionDetail("subOrder_lvl_1.Qty", "Qty")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child1_id])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())

    child_ord_id1 = request[child1_id.name]
    lvl2_details = OrdersDetails.create()
    lvl2_details.set_default_params(base_request)
    algo_split_man_extr_id = "order.direct"
    lvl2_details.set_extraction_id(algo_split_man_extr_id)
    lvl2_details.set_filter(["Order ID", child_ord_id1])

    call(Stubs.win_act_order_book.getChildOrdersDetails, lvl2_details.request())
    eq_wrappers.verify_order_value(base_request, case_id, 'Order ID', child_ord_id1, True)
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', '800', True)
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecPcy', 'DMA', True)
    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', True)
    # endregion
