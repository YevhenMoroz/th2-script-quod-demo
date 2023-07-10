from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX


class QAP_T8424(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_environment = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_environment, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.request_ack = FixMessageRequestForPositionsAckFX()
        self.position_report = FixMessagePositionReportFX()
        self.position_verifier = PositionVerifier(self.test_id)
        self.mass_cancel_request = FixPositionMassCancelRequestFX()
        self.trade_request = TradeEntryRequestFX()
        self.usd_cad = self.data_set.get_symbol_by_name("symbol_1")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.usd_cad
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clearing positions
        self.mass_cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.mass_cancel_request)
        self.sleep(5)
        # endregion
        # region Step 1 Crete position
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client,
                                                       "Currency": self.currency})
        self.trade_request.remove_fields_from_component("TradeEntryRequestBlock", ["SettlDate"])
        self.trade_request.change_instrument(self.usd_cad, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region Step 2 Send request for position
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        self.request_for_position.remove_parameter("SettlDate")
        self.fix_manager.send_message_and_receive_response(self.request_for_position)
        # endregion

        # region Step 3 Check position report ack
        self.request_ack.set_params_from_reqeust(self.request_for_position)
        self.fix_verifier.check_fix_message(self.request_ack)
        # endregion

        # region Step 4 Check position report
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("Currency", self.currency)
        self.fix_verifier.check_fix_message(self.position_report)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
