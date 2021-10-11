import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:

        order_book = FXOrderBook(case_id, case_base_request)
        order_book.set_filter(["Qty", "1000000"]).check_order_fields_list({"Sts": "1", "ExecSts": "2"})

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
