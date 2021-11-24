import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import m1_front_end, spo_front_end
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    near_qty = "2000000"
    far_qty = "3000000"
    near_date = spo_front_end()
    far_date = m1_front_end()
    case_base_request = get_base_request(session_id, case_id)

    try:

        rfq_tile = RFQTile(case_id, session_id)
        rfq_tile.crete_tile().modify_rfq_tile(near_qty=near_qty, far_qty=far_qty, far_tenor="1M")
        rfq_tile.check_qty(near_qty=near_qty, far_qty=far_qty)
        rfq_tile.check_tenor(near_tenor="Spot", far_tenor="1M")
        rfq_tile.modify_rfq_tile(near_qty="1000000")
        rfq_tile.check_date(near_date=near_date, far_date=far_date)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
