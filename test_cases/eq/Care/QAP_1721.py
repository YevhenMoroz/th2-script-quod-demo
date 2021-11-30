import logging

from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum


def execute(report_id, session_id):
    case_name = "QAP-1721"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "30"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    recipient = 'Desk of SalesDealers 1 (CL)'
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, 'Limit', 'Day', True, recipient, price, True,
                             DiscloseFlagEnum.MANUAL)
    # endregion

    # region accept order
    eq_wrappers.accept_order(lookup, qty, price)
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_ds = ExtractionDetail("order_ds", "DiscloseExec")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_ds
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("DiscloseFlag", order_ds.name, "M")
                                                  ]))
    # endregion
