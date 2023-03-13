import time
from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T10589(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.manual_settings_request = QuoteManualSettingsRequestFX(data_set=self.data_set)
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.dealer_intervention = None
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.account = self.data_set.get_client_by_name("client_mm_1")
        self.eur_gbp = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_2w_java = self.data_set.get_settle_type_ja_by_name('wk2')
        self.settle_type_1m_java = self.data_set.get_settle_type_ja_by_name('m1')
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.settle_type = self.data_set.get_settle_type_by_name("wk3")
        self.status_reject = Status.Reject
        self.instrument = {
            'Symbol': self.eur_gbp,
            'SecurityType': self.security_type,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 1
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_2w_java})
        self.manual_settings_request.set_executable_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(1)
        # endregion

        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], published=False)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 1
        self.manual_settings_request.set_pricing_off().set_executable_on()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(1)
        # endregion

        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], priced=False)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 1
        self.manual_settings_request.set_pricing_on().set_executable_on()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(1)
        # endregion

        # region Step 1
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1m_java})
        self.manual_settings_request.set_executable_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(1)
        # endregion
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], published=False)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
        # region Step 1
        self.manual_settings_request.set_pricing_off().set_executable_on()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(1)
        # endregion
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], priced=False)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints="*", SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

        # region Step 5
        self.manual_settings_request.set_pricing_on()
        self.java_manager.send_message(self.manual_settings_request)
        # endregion
        self.sleep(4)
