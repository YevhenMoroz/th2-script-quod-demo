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
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.HeldOrderAckRequestFX import HeldOrderAckRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiAutoHedgerMessages import RestApiAutoHedgerMessages


class QAP_T10780(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.rest_api_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_pos_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fix_pos_int_verifier = None
        self.position_verifier = PositionVerifier(self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.request_for_position_backup = FixMessageRequestForPositionsFX()
        self.position_report_ext = FixMessagePositionReportFX()
        self.position_report_int = FixMessagePositionReportFX()
        self.position_report_backup = FixMessagePositionReportFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.pos_report_none = FixMessageRequestForPositionsAckFX()
        self.trade_request = TradeEntryRequestFX()
        self.ack_request = HeldOrderAckRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.mo_order = FixMessageNewOrderSingleTakerDC()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_8")
        self.account_ext = self.data_set.get_account_by_name("account_mm_8")
        self.client_int = self.data_set.get_client_by_name("client_int_5")
        self.account_int = self.data_set.get_account_by_name("account_int_5")
        self.client_back_up = self.data_set.get_client_by_name("client_int_4")
        self.account_backup = self.data_set.get_account_by_name("account_int_4")
        self.auto_hedger_name = self.data_set.get_auto_hedger_by_name("auto_hedger_1")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_gbp
        }

        self.rest_api_ah_msg_1 = RestApiAutoHedgerMessages()
        self.rest_api_ah_msg_2 = RestApiAutoHedgerMessages()
        self.ah_params = None
        self.ah_params_2 = None
        self.expected_qty_int = "0"
        self.expected_qty_backup = "-1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check that they equal to 0
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_backup)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # reqeust for external client
        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_ext, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_ext)
        self.fix_pos_verifier.check_fix_message(self.pos_report_none,
                                                message_name=f"Check position for {self.client_ext} before start")
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)
        # reqeust for internal client
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "11")
        self.fix_pos_verifier.check_fix_message(self.pos_report_none,
                                                message_name=f"Check position for {self.client_int} before start")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # reqeust for backup client
        self.request_for_position_backup.set_default()
        self.request_for_position_backup.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                            "Account": self.client_back_up})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_backup, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_backup)
        self.fix_pos_verifier.check_fix_message(self.pos_report_none,
                                                message_name=f"Check position for {self.client_back_up} before start")
        self.request_for_position_backup.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_backup)
        self.sleep(1)

        # endregion
        # region Step 1
        self.rest_api_ah_msg_1.find_all_auto_hedger()
        self.ah_params = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_1)
        self.ah_params = self.rest_api_manager.parse_response_details(self.ah_params,
                                                                        {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == 'EUR/GBP':
                i["holdOrder"] = "true"
        self.rest_api_ah_msg_1.clear_message_params().modify_auto_hedger().set_params(self.ah_params)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_1)
        self.sleep(3)
        # endregion
        # region Step 3
        self.trade_request.set_default_params()
        self.trade_request.remove_fields_from_component("TradeEntryRequestBlock", ["SettlDate"])
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.client_ext})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_order_id = self.trade_request.get_ord_id_from_held(response)

        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters({"Account": self.client_int, "ClOrdID": ah_order_id})
        prefilter = {
            "header": {
                "MsgType": ("D", "EQUAL"),
                "TargetCompID": "QUOD8",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["Misc0"]
        self.fix_drop_copy_verifier.check_fix_message_sequence([self.ah_order, ],
                                                               key_parameters_list=[key_params],
                                                               pre_filter=prefilter,
                                                               message_name="Check that we create AH order and send child to market")
        # endregion
        # region Step 4
        self.ack_request.set_default_rej(ah_order_id)
        self.java_api_manager.send_message(self.ack_request)
        self.sleep(5)

        # reqeust for internal client
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        internal_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_int,
                                                                                   self.test_id)
        self.position_report_int.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "12")
        self.fix_pos_verifier.check_fix_message(self.position_report_int,
                                                message_name=f"Check position for {self.client_int} after")
        self.position_verifier.check_base_position(internal_report, self.expected_qty_int,
                                                   text=f"Check base for {self.client_int}")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # reqeust for backup client
        self.request_for_position_backup.set_default()
        self.request_for_position_backup.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                            "Account": self.client_back_up})
        backup_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_backup,
                                                                                 self.test_id)
        self.position_report_backup.set_params_from_reqeust(self.request_for_position_backup)
        self.position_report_backup.change_parameter("LastPositEventType", "12")
        self.position_report_backup.change_parameter("SettlDate", self.settle_date_spo)
        self.fix_pos_verifier.check_fix_message(self.position_report_backup,
                                                message_name=f"Check that date correctly transferred")
        self.position_verifier.check_base_position(backup_report, self.expected_qty_backup,
                                                   text=f"Check base for {self.client_back_up}")
        self.request_for_position_backup.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_backup)
        self.sleep(1)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_ah_msg_2.find_all_auto_hedger()
        self.ah_params_2 = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_2)
        self.ah_params_2 = self.rest_api_manager.parse_response_details(self.ah_params_2,
                                                                        {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params_2["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == 'EUR/GBP':
                i["holdOrder"] = "false"

        self.rest_api_ah_msg_2.clear_message_params().modify_auto_hedger().set_params(self.ah_params_2)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_2)
        self.sleep(3)
