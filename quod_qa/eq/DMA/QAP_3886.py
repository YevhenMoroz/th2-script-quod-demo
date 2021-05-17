import logging
from datetime import date

from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-3886"
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENTYMOROZ"
    lookup = "VETO"
    order_type = "Limit"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    today = date.today()
    weak = int(today.weekday())
    day = int(today.day)
    while weak < 4:
        day = day + 1
        weak = weak + 1
    expire_date = str(today.month) + '/' + str(day) + '/' + str(today.year)  # set saturday
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region  Create order

    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, "GoodTillDate",
                             price=price, expire_date=expire_date)
    # endregion
    # region Check values
    eq_wrappers.verify_value(base_request,case_id,"Sts","Open")
    eq_wrappers.verify_value(base_request, case_id, "Settle Date",  str(today.month) + '/' + str(day+3) + '/' + str(today.year))
    # endregion
