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


class QAP_T11502(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.pos_report = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.sec_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type,
            "Symbol": self.eur_gbp,
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 Send trade to have some position
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        response_eur_gbp = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id_eur_gbp = self.trade_request.get_exec_id(response_eur_gbp)
        # endregion

        # region Step 2 Subscribe to positions
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        self.request_for_position.change_parameter("Instrument", self.instrument)
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        self.sleep(5)
        self.pos_report.set_params_from_reqeust(self.request_for_position)
        self.pos_report.change_parameter("LastPositUpdateEventID", exec_id_eur_gbp)
        # endregion

        # region Step 3 Unsubscribe from positions
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
        # endregion

        # region Step 4 Check that we not receive position reports after unsubscription
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)

        prefilter = {
            "header": {
                "MsgType": ("AP", "EQUAL"),
                "TargetCompID": "PKSTH2",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["PosReqID"]
        self.fix_verifier.check_fix_message_sequence(
            fix_messages_list=[self.pos_report], key_parameters_list=[key_params], pre_filter=prefilter,
            message_name="Check that we receive oly 1 report")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
