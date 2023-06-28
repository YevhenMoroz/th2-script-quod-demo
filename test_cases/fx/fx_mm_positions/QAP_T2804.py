from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T2804(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.position_verifier = PositionVerifier(self.test_id)
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.trade_request = TradeEntryRequestFX()
        self.position_report = FixMessagePositionReportFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.usd_cad = self.data_set.get_symbol_by_name("symbol_12")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.usd_cad
        }
        self.qty_1 = "6000000"
        self.qty_2 = "2000000"
        self.qty_3 = "8000000"
        self.qty_4 = "3000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check Quote Position
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # endregion
        # region Step 1 Send buy order on 6M and check Quote Position(USD)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client,
                                                       "ExecQty": self.qty_1})
        self.trade_request.change_instrument(self.usd_cad, self.instr_type_spo)
        response = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.trade_request.get_exec_id(response)
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        position_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position)
        self.position_verifier.check_system_quote_position(position_report, self.trade_request)
        self.sleep(1)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
        # endregion

        # region Step 2 Send buy order on 2M and check Quote Position(USD)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client,
                                                       "ExecQty": self.qty_2})
        self.trade_request.change_instrument(self.usd_cad, self.instr_type_spo)
        response = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.trade_request.get_exec_id(response)
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        position_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position)
        self.position_verifier.check_system_quote_position(position_report, self.trade_request)
        self.sleep(1)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
        # endregion
        # region Step 3 Send sell order on 8M and check Quote Position(USD)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client,
                                                       "ExecQty": self.qty_3,
                                                       "Side": "S"})
        self.trade_request.change_instrument(self.usd_cad, self.instr_type_spo)
        response = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.trade_request.get_exec_id(response)
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        position_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position)
        self.position_verifier.check_system_quote_position(position_report, self.trade_request)
        self.sleep(1)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
        # endregion
        # region Step 4 Send sell order on 3M and check Quote Position(USD)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client,
                                                       "ExecQty": self.qty_4,
                                                       "Side": "S"})
        self.trade_request.change_instrument(self.usd_cad, self.instr_type_spo)
        response = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.trade_request.get_exec_id(response)
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        position_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position)
        self.position_verifier.check_system_quote_position(position_report, self.trade_request)
        self.sleep(1)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
