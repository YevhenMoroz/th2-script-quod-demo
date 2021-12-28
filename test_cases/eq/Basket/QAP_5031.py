import logging
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5031"
    # region Declarations
    client = "CLIENT_FIX_CARE"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    templ = {'Symbol': ['1', 'FR0004186856'], 'Quantity': ['2', '0'], 'Price': ['3', '0'],
             'Account': ['4', 'CLIENT_FIX_CARE_SA1'], 'Side': ['5', 'Buy'], 'OrdType': ['6', 'Limit'],
             'StopPrice': ['7', '0'], 'Capacity': ['8', 'Agency']}
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create basket template
    eq_wrappers.add_basket_template(base_request, "template by autotest", "templByAutotest", client, "Day", "Care",
                                    "ISIN",False,templ)
    # endregion
