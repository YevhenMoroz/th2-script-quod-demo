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


class QAP_T10885(TestCase):
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
        self.konstantin = self.data_set.get_client_by_name("client_mm_12")
        self.eur_gbp = self.data_set.get_symbol_by_name('symbol_3')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_type_bd = self.data_set.get_settle_type_by_name("broken")
        self.settle_date_bd = self.data_set.get_settle_date_by_name('broken_w1w2')
        self.instrument = {
            'Symbol': self.eur_gbp,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols = [{
            "Instrument": self.instrument,
            "SettlType": self.settle_type_bd,
            "SettlDate": self.settle_date_bd
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameters(
            {"BookType": "1", "NoRelatedSymbols": self.no_related_symbols, "SenderSubID": self.konstantin})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request,
                                                    ["1000000", "4000000", "5000000", "6000000", "11000000", "15000000"],
                                                    response=response[0])
        for i in range(12):
            self.md_snapshot.get_parameter("NoMDEntries")[i]["SettlDate"] = self.settle_date_bd
        self.fix_verifier.check_fix_message(self.md_snapshot)

        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameters(
            {"BookType": "0", "NoRelatedSymbols": self.no_related_symbols, "SenderSubID": self.konstantin})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request,
                                                    ["1000000", "3000000", "1000000", "1000000", "5000000", "4000000"],
                                                    response=response[0])
        for i in range(12):
            self.md_snapshot.get_parameter("NoMDEntries")[i]["SettlDate"] = self.settle_date_bd
        self.fix_verifier.check_fix_message(self.md_snapshot)

        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
