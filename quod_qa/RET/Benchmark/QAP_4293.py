import logging

from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_4303"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "100"
    qty = "200"
    tif = "Day"
    client = "HAKKIM"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregion

    # region Create order via FE
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif,
                             True, recipient, price, False, DiscloseFlagEnum.DEFAULT_VALUE, None)
    # endregion

    # region Check values in OrderBook according to 2nd step
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Sent")
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
