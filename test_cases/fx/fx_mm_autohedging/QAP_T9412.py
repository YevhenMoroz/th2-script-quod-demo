from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportDropCopyFX import FixMessageExecutionReportDropCopyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T9412(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.maintenance_request_ext = FixPositionMaintenanceRequestFX()
        self.maintenance_request_int = FixPositionMaintenanceRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_pos_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_drop_copy_verifier = None
        self.fix_pos_int_verifier = None
        self.position_verifier = PositionVerifier(self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.position_report_ext = FixMessagePositionReportFX()
        self.position_report_int = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.mo_order = FixMessageNewOrderSingleTakerDC()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_8")
        self.account_ext = self.data_set.get_account_by_name("account_mm_8")
        self.client_int = self.data_set.get_client_by_name("client_int_5")
        self.account_int = self.data_set.get_account_by_name("account_int_5")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_usd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check that they equal to 0
        self.maintenance_request_ext.set_default_params()
        self.maintenance_request_ext.change_account(self.account_ext)
        self.maintenance_request_ext.change_client(self.client_ext)
        self.maintenance_request_ext.change_instrument(self.eur_usd)
        self.java_api_manager.send_message(self.maintenance_request_ext)
        self.sleep(5)
        self.maintenance_request_int.set_default_params()
        self.maintenance_request_int.change_account(self.account_int)
        self.maintenance_request_int.change_client(self.client_int)
        self.maintenance_request_int.change_instrument(self.eur_usd)
        self.java_api_manager.send_message(self.maintenance_request_int)
        self.sleep(5)

        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "11")
        self.fix_pos_verifier.check_fix_message(self.position_report_ext,
                                                message_name=f"Check position for {self.client_ext} before start")
        self.position_verifier.check_base_position(external_report, "0", text=f"Check base for {self.client_ext}")
        self.sleep(1)
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)

        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        internal_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_int,
                                                                                   self.test_id)
        self.position_report_int.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "11")
        self.fix_pos_verifier.check_fix_message(self.position_report_int,
                                                message_name=f"Check position for {self.client_int} before start")
        self.position_verifier.check_base_position(internal_report, "0", text=f"Check base for {self.client_int}")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)

        # endregion
        # region Step 2
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"AccountGroupID": self.client_ext})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_exec_id = self.trade_request.get_ah_exec_id(response)
        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameter("ExecID", ah_exec_id)
        self.ah_exec_report.change_parameter("Account", self.account_int)
        ah_exec_params = ["ExecID"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report, key_parameters=ah_exec_params, message_name=
        "Check AutoHedger ExecutionReport")
        # self.sleep(3)

        # endregion
        # region Step 3-4
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameter("Account", self.client_int)
        self.mo_order.set_default_mo_from_trade(self.trade_request)
        self.mo_order.change_parameter("Account", self.client_int)
        prefilter = {
            "header": {
                "MsgType": ("D", "EQUAL"),
                "TargetCompID": "QUOD8",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["Misc0"]
        self.fix_drop_copy_verifier.check_fix_message_sequence([self.ah_order, self.mo_order],
                                                               key_parameters_list=[key_params, key_params],
                                                               pre_filter=prefilter,
                                                               message_name="Check that we create AH order and send child to market")

        # endregion
