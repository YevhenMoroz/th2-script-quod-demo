import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, RatesColumnNames, \
    PricingButtonColor
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    instrument = "EUR/USD-Spot"
    client_tier = "Silver"
    pips = "2"
    action = ClientPrisingTileAction
    cn = RatesColumnNames

    try:
        # Step 1
        rates_tile = ClientRatesTile(case_id, session_id)
        rates_tile.modify_client_tile(instrument=instrument, client_tier=client_tier, pips=pips)
        # Step 2-3
        rates_tile.select_rows([1])
        px_before = rates_tile.extract_values_from_rates(cn.ask_px, cn.bid_px, row_number=1)
        # Step 4
        rates_tile.modify_spread(action.widen_spread)
        px_after = rates_tile.extract_values_from_rates(cn.ask_px, cn.bid_px, row_number=1)

        expected_px = str(int(px_before[str(cn.ask_px)]) + (int(pips) * 10))
        rates_tile.compare_values(expected_value=expected_px, actual_value=px_after[str(cn.ask_px)],
                                  event_name="Check PX", value_name="Px Column")
        # Step 5
        rates_tile.check_color_on_lines(0, 90, expected_color=str(PricingButtonColor.yellow_button.value))
        # Step 6
        rates_tile.modify_spread(action.narrow_spread)
        px_after_2 = rates_tile.extract_values_from_rates(cn.ask_px, cn.bid_px, row_number=1)
        expected_px = str(int(px_after[str(cn.ask_px)]) - (int(pips) * 10))
        rates_tile.compare_values(expected_value=expected_px, actual_value=px_after_2[str(cn.ask_px)],
                                  event_name="Check PX", value_name="Px Column")
        # Step 7
        rates_tile.check_color_on_lines(0, 90, expected_color=str(PricingButtonColor.green_button.value))
        rates_tile.deselect_rows()
        rates_tile.press_use_default()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            rates_tile.close_tile()

        except Exception:
            logging.error("Error execution", exc_info=True)
