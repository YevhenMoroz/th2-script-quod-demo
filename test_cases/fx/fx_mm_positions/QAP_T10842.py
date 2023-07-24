from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.JavaApiVerifier import JavaApiVerifier
from test_framework.java_api_wrappers.fx.FixPositionReportFX import FixPositionReportFX
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T10842(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.java_verifier = JavaApiVerifier(self.java_api_env, self.test_id)
        self.request_for_position = FixRequestForPositionsFX()
        self.position_report = FixPositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "InstrType": self.instr_type_spo,
            "InstrSymbol": self.gbp_cad
        }
        self.position_verifier = PositionVerifier(self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id = self.trade_request.get_exec_id(response)
        trade_time = self.trade_request.get_termination_time(response)
        # endregion
        # region Step 2
        self.request_for_position.set_default_params()
        self.request_for_position.change_client(self.client)
        self.request_for_position.change_instrument(self.instrument, self.currency)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position, self.test_id)

        # endregion
        # region Step 3
        self.position_report.set_params_from_request(self.request_for_position)
        self.position_report.update_fields_in_component("PositionReportBlock", {"LastPositUpdateEventID": exec_id,
                                                                                "TransactTime": f">{trade_time}"})
        self.java_verifier.check_java_message(self.position_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.unsubscribe()
        self.java_api_manager.send_message(self.request_for_position)
