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
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T10613(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.maintenance_request = FixPositionMaintenanceRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_report = FixMessagePositionReportFX()
        self.position_report_2 = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.listing_gbp_cad = self.data_set.get_listing_id_by_name("gbp_cad_spo")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.sec_type = self.data_set.get_security_type_by_name("fx_spot")
        self.sec_type_java = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type,
            "Symbol": self.gbp_cad
        }
        self.settle_date = self.data_set.get_settle_date_by_name("spot")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id = self.trade_request.get_exec_id(response)
        self.sleep(3)
        # endregion
        # region Step 2
        self.request_for_position.set_default()
        self.request_for_position.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                     "Account": self.client})
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)

        self.maintenance_request.set_default_params()
        self.maintenance_request.change_account(self.account)
        self.maintenance_request.change_client(self.client)
        self.maintenance_request.remove_settle_date()
        self.maintenance_request.change_instrument(self.gbp_cad, self.sec_type_java)
        self.java_api_manager.send_message(self.maintenance_request)
        self.sleep(1)
        # endregion
        # region Step 3
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("LastPositUpdateEventID", exec_id)
        self.position_report.change_parameter("SettlDate", self.settle_date)
        self.position_report.change_parameter("LastPositEventType", "5")
        self.position_report_2.set_params_from_reqeust(self.request_for_position)
        self.position_report_2.change_parameter("SettlDate", self.settle_date)
        self.position_report_2.change_parameter("LastPositEventType", "11")
        prefilter = {
            "header": {
                "MsgType": ("AP", "EQUAL"),
                "TargetCompID": "PKSTH2",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["PosReqID"]

        self.fix_verifier.check_fix_message_sequence([self.position_report, self.position_report_2],
                                                     key_parameters_list=[key_params, key_params],
                                                     pre_filter=prefilter,
                                                     message_name="Check that we receive 2 reports")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
