import logging
from datetime import datetime
from th2_grpc_hand import rhbatch_pb2

from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1047"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    qty_percent = "100"
    price = "30"
    client = "CLIENT1"
    lookup = "VETO.[PARIS]"
    handl_ins = 2  # Care
    order_type = 2  # Limit
    side = 2  # Buy
    tif = 0  # Day

    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create CO
    eq_wrappers.create_order_via_fix(case_id, handl_ins, side, client, order_type, qty, tif, price)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_pts = ExtractionDetail("order_pts", "PostTradeStatus")
    order_dfd = ExtractionDetail("order_dfd", "DoneForDay")
    order_es = ExtractionDetail("order_es", "ExecSts")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_pts,
                                                                                            order_dfd,
                                                                                            order_es
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent")
                                                  ]))
    # endregion

    # region Direct order
    eq_wrappers.direct_order(lookup, price, qty, qty_percent)
    # endregion

    # check sub Order status

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
    call(act.getChildOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking Child order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent('Qty', order_qty.name, str(int(int(qty)/2))),
                                                  ]))
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
