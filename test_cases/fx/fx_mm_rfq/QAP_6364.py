from pathlib import Path
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.base_window import decorator_try_except


class QAP_6364(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.fix_manager_rfq = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.market_data_snap_shot = None
        self.md_req_id = None

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def pre_conditions_and_run(self):
        account = self.data_set.get_client_by_name("client_3")
        symbol = self.data_set.get_symbol_by_name("gbp_usd")
        security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        qty = random_qty(1, 2, 7)
        instrument = {
            "Symbol": symbol,
            "SecurityType": security_type_fwd
        }
        self.md_req_id = "GBP/USD:FXF:WK1:HSBC"
        # Step 1
        self.market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data_fwd()
        self.market_data_snap_shot.change_parameters({"Instrument": instrument})
        self.market_data_snap_shot.update_value_in_repeating_group("NoMDEntries", "MDQuoteType", 0)
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
        # Step 2
        quote_request = FixMessageQuoteRequestFX().set_rfq_params_fwd()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="GBP", Instrument=instrument, OrderQty=qty)
        self.fix_manager_rfq.send_message(quote_request, "Send Quote Request")
        # TODO Check QuoteRequestBook

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def post_conditions(self):
        self.market_data_snap_shot.set_market_data_fwd()
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
