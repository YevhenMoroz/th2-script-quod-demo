import logging
import os
from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base

from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

case_name = os.path.basename(__file__)

def execute(report_id, session_id):
    try:
        # region Declarations
        lookup = "BARC.L"   
        order_type = "Limit"
        price = "1"
        qty = "1000"
        tif = "Day"
        client = "CLIENT2"
        # endregion

        # region Open FE
        case_id = create_event(case_name, report_id)
        set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)
        # endregion

        # region Create order via FE according to 1st and 2nd steps
        eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif,
                                False, None, price, False, False, None)
        # endregion

        # region Check values in OrderBook
        eq_wrappers.verify_value(base_request, case_id, "Sts", "Open")
        # endregion
    except:
        logging.error("Error execution",exc_info=True)
