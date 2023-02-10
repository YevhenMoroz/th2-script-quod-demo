from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty, check_quote_request_id, extract_freenotes
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2537(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_request_book = None
        self.account = self.data_set.get_client_by_name("client_mm_2")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_w1 = self.data_set.get_settle_date_by_name("wk1")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }
        self.text = "no bid forward points for client tier `2600011' on GBP/USD WK1 on QUODFX - manual intervention required"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_symbol=self.symbol)
        self.quote_request.update_far_leg(leg_symbol=self.symbol)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="GBP", Instrument=self.instrument)
        self.fix_manager_gtw.send_message(self.quote_request)
        self.sleep(2)
        notes = extract_freenotes(self.quote_request)
        self.verifier = Verifier(self.test_id)
        self.verifier.set_event_name("Compare notes")
        self.verifier.compare_values("CompareNotes", self.text, notes)
        self.verifier.verify()
