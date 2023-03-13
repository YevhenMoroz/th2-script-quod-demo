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
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T2801(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.manual_settings_request = QuoteManualSettingsRequestFX(data_set=self.data_set)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_type_1w = self.data_set.get_settle_type_by_name('wk1')
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.manual_settings_request.set_default_params().set_executable_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(4)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameter("BookType", "1")
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "*"], published=False)
        self.md_snapshot.get_parameter("NoMDEntries").pop(7)
        self.md_snapshot.get_parameter("NoMDEntries").pop(6)
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
        #     "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
        #     "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
        #     "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
        #     "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)

        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 1
        self.manual_settings_request.set_pricing_off().set_executable_on()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(4)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameter("BookType", "1")
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "*"], priced=False)
        self.md_snapshot.get_parameter("NoMDEntries").pop(7)
        self.md_snapshot.get_parameter("NoMDEntries").pop(6)
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
        #     "SettlType", "MDEntryTime", "MDEntryPx", "QuoteCondition", "MDQuoteType", "MDOriginType", "MDEntryID",
        #     "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
        #     "SettlType", "MDEntryTime", "MDEntryPx", "QuoteCondition", "MDQuoteType", "MDOriginType", "MDEntryID",
        #     "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)

        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 5
        self.manual_settings_request.set_pricing_on()
        self.java_manager.send_message(self.manual_settings_request)
        # endregion
        self.sleep(4)
