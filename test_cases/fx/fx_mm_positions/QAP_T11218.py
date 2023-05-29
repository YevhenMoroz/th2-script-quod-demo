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


class QAP_T11218(TestCase):
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
        self.pos_report_gbp_cad = FixMessagePositionReportFX()
        self.pos_report_eur_gbp = FixMessagePositionReportFX()
        self.pos_report_gbp_cad_after = FixMessagePositionReportFX()
        self.pos_report_eur_gbp_after = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")

        self.currency_eur = self.data_set.get_currency_by_name("currency_eur")
        self.currency_gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")

        self.settle_date_wk1_java = self.data_set.get_settle_date_by_name("spot_java_api")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("spot")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.instr_type_spo)
        response_gbp_cad = self.java_api_manager.send_message_and_receive_response(self.trade_request)

        exec_id_gbp_cad = self.trade_request.get_exec_id(response_gbp_cad)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        response_eur_gbp = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id_eur_gbp = self.trade_request.get_exec_id(response_eur_gbp)
        # endregion

        # region Step 3
        self.request_for_position.set_params_for_date(self.settle_date_wk1)
        self.request_for_position.change_parameter("Account", self.client)
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        self.sleep(5)
        # endregion

        # region Step 4
        self.pos_report_gbp_cad.set_params_for_all(self.request_for_position)
        self.pos_report_gbp_cad.change_parameter("LastPositUpdateEventID", exec_id_gbp_cad)
        self.pos_report_eur_gbp.set_params_for_all(self.request_for_position)
        self.pos_report_eur_gbp.change_parameter("LastPositUpdateEventID", exec_id_eur_gbp)
        self.pos_report_gbp_cad_after.set_params_for_all(self.request_for_position)
        self.pos_report_gbp_cad_after.change_parameter("LastPositEventType", "13")
        self.pos_report_gbp_cad_after.remove_parameter("TransactTime")
        self.pos_report_eur_gbp_after.set_params_for_all(self.request_for_position)
        self.pos_report_eur_gbp_after.change_parameter("LastPositEventType", "13")
        self.pos_report_eur_gbp_after.remove_parameter("TransactTime")
        prefilter = {
            "header": {
                "MsgType": ("AP", "EQUAL"),
                "TargetCompID": "PKSTH2",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["PosReqID"]

        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)

        self.fix_verifier.check_fix_message_sequence(
            fix_messages_list=[self.pos_report_gbp_cad,
                               self.pos_report_eur_gbp,
                               self.pos_report_gbp_cad_after,
                               self.pos_report_eur_gbp_after],
            key_parameters_list=[key_params, key_params, key_params, key_params],
            pre_filter=prefilter,
            message_name="Check that we receive 4 reports")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(5)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
