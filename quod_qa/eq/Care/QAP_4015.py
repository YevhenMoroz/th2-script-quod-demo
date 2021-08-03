import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
def execute(report_id, session_id):
    case_name = "QAP-4015"
    # region Declarations
    act = Stubs.win_act_order_book
    qty = "900"
    price = "40"
    client = "CLIENT_FIX_CARE"
    last_mkt = 'DASI'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create order via fix
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id2 = eq_wrappers.get_order_id(base_request)
    # endregion

    eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)

    # region manual_cross
    eq_wrappers.manual_cross_orders(base_request, qty, price, (1, 2), last_mkt)
    # endregion
    # region check order1
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled')
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', qty)
    # endregion
    order_info_extraction_cancel = "getOrderInfo_cancelled"
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(order_info_extraction_cancel)
    main_order_details.set_filter(["Order ID", order_id2])
    call(act.getOrdersDetails, main_order_details.request())
    # region check order2
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled')
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', qty)
    # endregion