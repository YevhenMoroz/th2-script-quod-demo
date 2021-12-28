import logging
from test_framework.old_wrappers import eq_wrappers
from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4331"

    # region Declarations
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    qty = "100"
    price = "100"
    client = "MOClient"
    account = "MOClient_SA1"
    account2 = "MOClient_SA2"
    washbook = "DMA Washbook"
    washbook2 = "CareWB"
    lookup = "VETO"
    order_type = "Limit"
    tif = "Day"
    # endregion

    # Create order with account and washbook
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, is_sell=False, price=price, washbook=washbook, account=account)

    # Checks in Order book
    eq_wrappers.verify_order_value(request=base_request, case_id=case_id, column_name="Wash Book", expected_value=washbook)
    eq_wrappers.verify_order_value(request=base_request, case_id=case_id, column_name="Account ID", expected_value=account)

    # Amend order (account and washbook)
    eq_wrappers.amend_order(request=base_request, parent_event=case_id, account=account2, washbook=washbook2)


    # Checks in Order book
    eq_wrappers.verify_order_value(request=base_request, case_id=case_id, column_name="Wash Book", expected_value=washbook2)
    eq_wrappers.verify_order_value(request=base_request, case_id=case_id, column_name="Account ID", expected_value=account2)

