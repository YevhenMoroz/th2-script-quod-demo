import logging

from datetime import datetime

from test_cases.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps

from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1016"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    order_type = "Limit"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id,report_id,case_id,work_dir,username,password)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username,
                             price=price,recipient_user=True)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
    eq_wrappers.verify_order_value(base_request, case_id, "Client Name", client)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
