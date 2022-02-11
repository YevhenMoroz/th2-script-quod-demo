import logging
from datetime import datetime
import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from pathlib import Path
from test_framework.core.test_case import TestCase
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1020(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        client = "CLIENT_FIX_CARE"
        time = datetime.utcnow().isoformat()
        lookup = "VETO"
        # endregion
        # region Open FE
        qty = "900"
        qty2 = "400"
        price = "20"
        price2 = "50"
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # region Create CO
        test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
        # endregion
        open_fe(session_id, report_id, case_id, work_dir, username)
        # endregion
        # region Check values in OrderBook
        eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
        eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
        eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)
        before_order_details_id = "before_order_details"

        # endregion
        # region Accept CO
        eq_wrappers.accept_order(lookup, qty, price)
        # endregion
        # region Check values in OrderBook after Accept
        eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
        # endregion
        # region Amend order
        eq_wrappers.amend_order(base_request, qty=qty2, price=price2)
        # endregion
        # region Check values after Amend
        eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
        eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty2)
        eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price2)
        # endregion
        # region Cancelling order
        eq_wrappers.cancel_order(base_request)
        # endregion
        # region Check values after Cancel
        eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Cancelled")
        # endregion
        logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
