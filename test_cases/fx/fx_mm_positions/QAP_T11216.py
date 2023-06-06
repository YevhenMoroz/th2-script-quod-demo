from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.JavaApiVerifier import JavaApiVerifier
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.java_api_wrappers.pks_messages.FixRequestForPositionsAck import FixRequestForPositionsAck


class QAP_T11216(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.java_api_verifier = JavaApiVerifier(self.java_api_env, self.test_id)
        self.request_for_position = FixRequestForPositionsFX()
        self.report = FixRequestForPositionsAck()
        self.trade_request = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.sec_type_java = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "InstrType": self.sec_type_java,
            "InstrSymbol": self.gbp_cad
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.sec_type_java)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region Step 2
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # endregion

        # region Step 3
        self.request_for_position.set_default_params()
        self.request_for_position.change_client(self.client)
        self.request_for_position.change_instrument(self.instrument, self.currency)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        # endregion
        # region Step 4
        self.report.set_params_from_request_sub(self.request_for_position)
        self.java_api_verifier.check_java_message(self.report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.unsubscribe()
        self.java_api_manager.send_message(self.request_for_position)
