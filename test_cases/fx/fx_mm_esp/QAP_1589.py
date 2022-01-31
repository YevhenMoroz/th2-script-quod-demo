import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames, ClientPrisingTileAction
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from win_gui_modules.order_book_wrappers import ExtractionDetail
from datetime import datetime, timedelta

#
#
# def create_or_get_rates_tile(base_request, service):
#     call(service.createRatesTile, base_request.build())
#
#
# def modify_rates_tile(base_request, service, instrument, client, pips):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     modify_request.set_instrument(instrument)
#     modify_request.set_client_tier(client)
#     modify_request.set_pips(pips)
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def modify_spread(base_request, service, *args):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     if "increase_ask" in args:
#         modify_request.increase_ask()
#     if "decrease_ask" in args:
#         modify_request.decrease_ask()
#     if "increase_bid" in args:
#         modify_request.increase_bid()
#     if "decrease_bid" in args:
#         modify_request.decrease_bid()
#     if "narrow_spread" in args:
#         modify_request.narrow_spread()
#     if "widen_spread" in args:
#         modify_request.widen_spread()
#     if "skew_towards_ask" in args:
#         modify_request.skew_towards_ask()
#     if "skew_towards_bid" in args:
#         modify_request.skew_towards_bid()
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def live_toggle(base_request, service):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     modify_request.toggle_live()
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def use_defaults_click(base_request, service):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     modify_request.press_use_defaults()
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def extract_column_base(base_request, service):
#     from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, DeselectRowsRequest
#     extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
#     extraction_id = bca.client_orderid(4)
#     extract_table_request.set_extraction_id(extraction_id)
#     extract_table_request.set_row_number(1)
#     extract_table_request.set_bid_extraction_field(ExtractionDetail("bid", "Base"))
#     extract_table_request.set_ask_extraction_field(ExtractionDetail("ask", "Base"))
#     response = call(service.extractRatesTileTableValues, extract_table_request.build())
#     deselect_rows_request = DeselectRowsRequest(details=base_request)
#     call(service.deselectRows, deselect_rows_request.build())
#     return response
#
#
# def check_margins(case_id, initial_margin, changed_margin, live_margin, live_off_margin, use_default_margin):
#     verifier = Verifier(case_id)
#     verifier.set_event_name("Checking margins bid")
#     verifier.compare_values(f'After live toggle off', initial_margin.get('bid'), live_off_margin.get('bid'))
#     verifier.compare_values(f'After live toggle on', changed_margin.get('bid'), live_margin.get('bid'))
#     verifier.compare_values(f'After use defaults', initial_margin.get('bid'), use_default_margin.get('bid'))
#     verifier.verify()
#
#     verifier.set_event_name("Checking margins ask")
#     verifier.compare_values(f'After live toggle off', initial_margin.get('ask'), live_off_margin.get('ask'))
#     verifier.compare_values(f'After live toggle on', changed_margin.get('ask'), live_margin.get('ask'))
#     verifier.compare_values(f'After use defaults', initial_margin.get('ask'), use_default_margin.get('ask'))
#     verifier.verify()
#
#
# def execute(report_id, session_id):
#     start = datetime.now()
#     case_name = Path(__file__).name[:-3]
#     case_id = bca.create_event(case_name, report_id)
#
#     set_base(session_id, case_id)
#
#     cp_service = Stubs.win_act_cp_service
#
#     case_base_request = get_base_request(session_id=session_id, event_id=case_id)
#     base_details = BaseTileDetails(base=case_base_request)
#
#     instrument = "EUR/USD-Spot"
#     client_tier = "Silver"
#     pips = "50"
#
#     try:
#
#         # Step 1
#
#         create_or_get_rates_tile(base_details, cp_service)
#         modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)
#
#         # Step 2
#
#         initial_margin = extract_column_base(base_details, cp_service)
#         modify_spread(base_details, cp_service, "widen_spread")
#         modified_margin = extract_column_base(base_details, cp_service)
#
#         # Step 3
#
#         live_toggle(base_details, cp_service)
#         live_toggle_off_margin = extract_column_base(base_details, cp_service)
#
#         # Step 4
#
#         live_toggle(base_details, cp_service)
#         live_toggle_on_margin = extract_column_base(base_details, cp_service)
#
#         # Step 5
#
#         use_defaults_click(base_details, cp_service)
#         use_default_margin = extract_column_base(base_details, cp_service)
#
#         # Step 6
#
#         check_margins(
#             case_id, initial_margin, modified_margin,
#             live_toggle_on_margin, live_toggle_off_margin, use_default_margin
#         )
#
#     except Exception:
#         logging.error("Error execution", exc_info=True)
#         bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
#     finally:
#         try:
#             # Close tile
#             print(f'{case_name} duration time = ' + str(datetime.now() - start))
#             call(cp_service.closeRatesTile, base_details.build())
#         except Exception:
#             logging.error("Error execution", exc_info=True)
pips = "50"
ask_base = RatesColumnNames.ask_base
bid_base = RatesColumnNames.bid_base
action = ClientPrisingTileAction.widen_spread


class QAP_1589(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Initialization
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        # endregion
        # region Variables
        client = self.data_set.get_client_tier_by_name("client_tier_1")
        symbol = self.data_set.get_symbol_by_name("symbol_1")
        instrument = symbol + "-Spot"
        # end region
        # region Step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=instrument, client_tier=client)
        self.rates_tile.press_use_default()
        base_before = self.rates_tile.extract_values_from_rates(bid_base, ask_base)
        # endregion
        # region Step 2
        self.rates_tile.modify_client_tile(pips=pips)
        self.rates_tile.modify_spread(action)
        base_after = self.rates_tile.extract_values_from_rates(bid_base, ask_base)
        expected_after = str(int(base_before[str(bid_base)]) + int(pips))
        self.rates_tile.compare_values(expected_after, base_after[str(bid_base)],
                                       event_name="Check that values change after modify spread")
        # endregion
        # region Step 3
        self.rates_tile.press_live()
        base_with_live = self.rates_tile.extract_values_from_rates(bid_base, ask_base)
        self.rates_tile.compare_values(base_with_live[str(bid_base)], base_before[str(bid_base)],
                                       event_name="Values after enable live")
        # endregion
        # region Step 4
        self.rates_tile.press_live()
        base_without_live = self.rates_tile.extract_values_from_rates(bid_base, ask_base)
        self.rates_tile.compare_values(base_after[str(bid_base)], base_without_live[str(bid_base)],
                                       event_name="Values after disable live")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
