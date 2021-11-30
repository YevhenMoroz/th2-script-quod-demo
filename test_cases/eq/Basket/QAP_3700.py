import logging
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3700"
    # region Declarations
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    template = "templ"
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Precondition
    eq_wrappers.add_basket_template(base_request, template)
    # endregion
    # region remove template
    eq_wrappers.remove_basket_template(base_request, template)
    # endregion
