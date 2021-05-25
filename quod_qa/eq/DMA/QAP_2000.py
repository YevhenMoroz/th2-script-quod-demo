import logging
from datetime import datetime
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import set_base
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2000"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    client = "CLIENTYMOROZ"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    # endregion
    # region Create order via FIX
    fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 0)
    response = fix_message.pop('response')
    # endregion
    # region Check values in OrderBook
    fix_verifier = FixVerifier('fix-bs-310-columbia', case_id)

    params = {
        'Account': client + "_PARIS",
        'OrderQty': qty,
        'Side': 2,
        'TimeInForce': 0,
        'TransactTime': '*',
        'SettlDate': '*',
        'Currency': '*',
        'SettlType': '*',
        'HandlInst': '*',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'NoParty': '*',
        'Instrument': '*',
        'ExDestination': '*'
    }
    fix_verifier.CheckNewOrderSingle(params, response)
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
