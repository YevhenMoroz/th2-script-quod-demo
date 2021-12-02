import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import m1_front_end, spo_front_end
from test_framework.win_gui_wrappers.data_set import ClientPrisingTileAction, PriceNaming, PricingButtonColor, \
    RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
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
    pn = PriceNaming
    cn = RatesColumnNames

    try:

        rfq_tile = RFQTile(case_id, session_id)
        rfq_tile.crete_tile().modify_rfq_tile(near_qty=near_qty, far_qty=far_qty, far_tenor="1M")
        rfq_tile.check_qty(near_qty=near_qty, far_qty=far_qty)
        rfq_tile.check_tenor(near_tenor="Spot", far_tenor="1M")
        rfq_tile.modify_rfq_tile(near_qty="1000000")
        rfq_tile.check_date(near_date=near_date, far_date=far_date)
        rates_tile = ClientRatesTile(case_id, session_id)
        # rates_tile.modify_client_tile(instrument="EUR/USD-SPOT", client_tier="Gold_day", pips="5")
        # rates_tile.modify_spread(ClientPrisingTileAction.widen_spread)
        # rates_tile.check_color_on_lines(0, 90, expected_color=PricingButtonColor.yellow_button.value)
        # px = rates_tile.extract_values_from_rates(cn.ask_px)
        # px = rates_tile.extract_base()
        # print(px)
        effective = rates_tile.extract_values_from_rates(cn.ask_px, cn.bid_px)
        print(effective)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
