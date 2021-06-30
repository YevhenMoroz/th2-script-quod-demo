import logging
import os
from datetime import datetime, date, timedelta

from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_4301_fix"
    seconds, nanos = timestamps()  # Store case start time

    connectivity_buy_side = "fix-bs-310-columbia"
    connectivity_sell_side = "fix-ss-310-columbia-standart"

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = ["1300", "1500"]
    price = "20"
    expire_date = date.today() + timedelta(2)
    time = datetime.utcnow().isoformat()
    # endregion

    # region Open FE
    case_id = bca.create_event(os.path.basename(__file__), report_id)

    fix_manager_310 = FixManager(connectivity_sell_side, case_id)
    fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

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

    # region Create order via FIX
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia", "XLON_CLIENT1",
                                                                         "XLON", 20)

    fix_manager_qtwquod5 = FixManager(connectivity_buy_side, case_id)


    fix_params = {
        'Account': "CLIENT1",
        'HandlInst': "1",
        'Side': "2",
        'OrderQty': "1300",
        'TimeInForce': "6",
        'ExpireDate': expire_date.strftime("%Y%m%d"),
        'OrdType': "2",
        'Price': price,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'GB00B0J6N107_GBP',
            'SecurityID': 'GB00B0J6N107',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XLON'
        },
        'Currency': 'GBP'
    }

    fix_message = FixMessage(fix_params)

    fix_message.add_random_ClOrdID()
    response = fix_message.pop('response')
    fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message)
    # end region

    # Check on ss
    params = {
        'OrderQty': qty,
        'ExecType': '3',
        'OrdStatus': '1',
        'Side': 2,
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
    }
    print(response.response_messages_list[0].fields['ClOrdID'].simple_value)
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
