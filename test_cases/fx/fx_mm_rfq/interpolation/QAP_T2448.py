from pathlib import Path
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.core.try_exept_decorator import try_except
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX


class QAP_T2448(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixQuoteRequestFX()
        self.fix_manager_rfq = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_req_id = "GBP/USD:FXF:WK1:HSBC"
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.note = "WK1 is not executable - manual intervention required"
        self.expected_quoting = "N"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Step 1
        self.market_data_snap_shot.set_market_data_fwd()
        self.market_data_snap_shot.change_parameters({"Instrument": self.instrument})
        self.market_data_snap_shot.update_value_in_repeating_group("NoMDEntries", "MDQuoteType", 0)
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
        # Step 2
        self.sleep(2)
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.change_client(self.account)
        self.quote_request.change_instr_symbol(self.symbol, self.currency)
        response: list = self.java_api_manager.send_message_and_receive_response(self.quote_request, response_time=25000)
        received_notes = response[-1].get_parameter("QuoteRequestNotifBlock")["FreeNotes"]
        received_quoting = response[-1].get_parameter("QuoteRequestNotifBlock")["AutomaticQuoting"]
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check FreeNotes and AutomaticQuoting")
        self.verifier.compare_values("Free notes", self.note, received_notes)
        self.verifier.compare_values("AutomaticQuoting", self.expected_quoting, received_quoting)
        self.verifier.verify()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Step 3
        self.market_data_snap_shot.set_market_data_fwd()
        self.market_data_snap_shot.change_parameters({"Instrument": self.instrument})
        self.market_data_snap_shot.update_MDReqID(self.md_req_id, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.market_data_snap_shot, "Send MD GBP/USD FWD HSBC")
