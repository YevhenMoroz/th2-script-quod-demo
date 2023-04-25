import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T8824(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.adjustment_request = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.silver_id = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.oos = self.data_set.get_client_by_name("client_mm_13")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_1w_java = self.data_set.get_settle_type_ja_by_name("wk1")
        self.settle_type_fwd = self.data_set.get_settle_type_by_name("wk1")
        self.no_related_symbols_fwd = [{"Instrument": {
            "Symbol": self.eur_usd,
            "SecurityType": self.security_type_fwd,
            "Product": "4", },
            "SettlType": self.settle_type_fwd}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region 1-2
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.oos).change_parameter(
            "NoRelatedSymbols", self.no_related_symbols_fwd)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        default_bid_px_3 = response[0].get_parameter("NoMDEntries")[4]["MDEntryPx"]
        default_ask_px_3 = response[0].get_parameter("NoMDEntries")[5]["MDEntryPx"]
        # endregion

        # region 3-4
        self.adjustment_request.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                          {"InstrSymbol": self.eur_usd,
                                                                           "ClientTierID": self.silver_id,
                                                                           "Tenor": self.settle_type_1w_java})
        self.adjustment_request.update_margins_by_index(3, "-0.2", "0")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(4)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.oos).change_parameter(
            "NoRelatedSymbols", self.no_related_symbols_fwd)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px_3 = round(float(default_bid_px_3) + 0.00002, 5)
        modified_ask_px_3 = round(float(default_ask_px_3), 5)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryPx=modified_bid_px_3)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryPx=modified_ask_px_3)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

        # region 4

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.adjustment_request.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                          {"InstrSymbol": self.eur_usd,
                                                                           "ClientTierID": self.silver_id,
                                                                           "Tenor": self.settle_type_1w_java})
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(2)
