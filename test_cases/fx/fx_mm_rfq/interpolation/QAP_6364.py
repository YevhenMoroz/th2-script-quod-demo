from pathlib import Path
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, QuoteRequestBookColumns


class QAP_6364(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_rfq = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_req_id = "GBP/USD:FXF:WK1:HSBC"
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.qty = "1000000"
        self.qty_col = QuoteRequestBookColumns.qty.value
        self.notes_col = QuoteRequestBookColumns.free_notes.value
        self.inst_col = QuoteRequestBookColumns.instrument_symbol.value
        self.note = "WK1 is not executable - manual intervention required"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Step 1
        self.market_data_snap_shot.set_market_data_fwd()
        self.market_data_snap_shot.change_parameters({"Instrument": self.instrument})
        self.market_data_snap_shot.update_value_in_repeating_group("NoMDEntries", "MDQuoteType", 0)
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
        # Step 2
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_rfq_params_fwd()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency="GBP", Instrument=self.instrument, OrderQty=self.qty)
        self.fix_manager_rfq.send_message(quote_request, "Send Quote Request")

        self.quote_request_book.set_filter([self.qty_col, self.qty, self.inst_col, self.symbol]). \
            check_quote_book_fields_list({self.notes_col: self.note})

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Step 3
        self.market_data_snap_shot.set_market_data_fwd()
        self.market_data_snap_shot.change_parameters({"Instrument": self.instrument})
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
