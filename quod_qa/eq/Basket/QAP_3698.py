import logging
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3698"
    # region Declarations
    client = "CLIENT_FIX_CARE"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    templ = {'Symbol': ['Symbol', 'FR0004186856'], 'Quantity': ['Quantity', '0'], 'Price': ['Price', '0'],
             'Account': ['Account', 'CLIENT_FIX_CARE_SA1'], 'Side': ['Side', 'Buy'], 'OrdType': ['OrdType', 'Limit'],
             'StopPrice': ['StopPrice', '0'], 'Capacity': ['Capacity', 'Agency']}
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create basket template
    eq_wrappers.add_basket_template(base_request, "template by autotest", "templByAutotest", client, "Day", "Care",
                                    "ISIN",True,templ)
    # endregion
