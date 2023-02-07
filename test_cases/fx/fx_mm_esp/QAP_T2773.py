import time
from pathlib import Path
from custom import basic_custom_actions as bca
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
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T2773(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.silver_id = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_type_1w = self.data_set.get_settle_type_by_name('wk1')
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.quote_adjustment_entry_list = {
            "QuoteAdjustmentEntryBlock":
                [{"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
                  "IndiceUpperQty": "1"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "2"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "3"}

                 ]}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id,
             "QuoteAdjustmentEntryList": self.quote_adjustment_entry_list})
        self.java_manager.send_message(self.quote_adjustment)
        time.sleep(2)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameter("BookType", "1")
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "2000000", "10000000", "*"], published=False,
                                                    band_not_pub=["pub", "2000000", "10000000", "pub"])
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.quote_adjustment.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                        {"InstrSymbol": self.eur_usd,
                                                                         "ClientTierID": self.silver_id})
        self.java_manager.send_message(self.quote_adjustment)
        self.md_request.set_md_uns_parameters_maker()
        self.sleep(2)
