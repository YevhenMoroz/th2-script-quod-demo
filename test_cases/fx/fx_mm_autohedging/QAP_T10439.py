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
from test_framework.java_api_wrappers.fx.HeldOrderAckRequestFX import HeldOrderAckRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiAutoHedgerMessages import RestApiAutoHedgerMessages


class QAP_T10439(TestCase):
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
        self.maintenance_request_ext = FixPositionMaintenanceRequestFX()
        self.maintenance_request_int = FixPositionMaintenanceRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_pos_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fix_pos_int_verifier = None
        self.position_verifier = PositionVerifier(self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.position_report_ext = FixMessagePositionReportFX()
        self.position_report_int = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.ack_request = HeldOrderAckRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.mo_order = FixMessageNewOrderSingleTakerDC()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_8")
        self.account_ext = self.data_set.get_account_by_name("account_mm_8")
        self.client_int = self.data_set.get_client_by_name("client_int_5")
        self.account_int = self.data_set.get_account_by_name("account_int_5")
        self.auto_hedger_name = self.data_set.get_auto_hedger_by_name("auto_hedger_1")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.listing_eur_gbp = self.data_set.get_listing_id_by_name("eur_gbp_spo")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_gbp
        }

        self.rest_api_ah_msg_1 = RestApiAutoHedgerMessages()
        self.rest_api_ah_msg_2 = RestApiAutoHedgerMessages()
        self.rest_api_ah_msg_3 = RestApiAutoHedgerMessages()
        self.ah_params = None
        self.ah_params_2 = None
        self.ah_params_3 = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Set holdOrder to false
        self.rest_api_ah_msg_1.find_all_auto_hedger()
        self.ah_params = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_1)
        self.ah_params = self.rest_api_manager.parse_response_details(self.ah_params,
                                                                      {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == 'EUR/GBP':
                i["holdOrder"] = "false"
        self.rest_api_ah_msg_1.clear_message_params().modify_auto_hedger().set_params(self.ah_params)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_1)
        self.sleep(3)
        # endregion
        # region Clear position before start and check that they equal to 0
        self.maintenance_request_ext.set_default_params()
        self.maintenance_request_ext.change_account(self.account_ext)
        self.maintenance_request_ext.change_client(self.client_ext)
        self.maintenance_request_ext.change_instrument(self.eur_gbp)
        self.java_api_manager.send_message(self.maintenance_request_ext)
        self.sleep(5)
        self.maintenance_request_int.set_default_params()
        self.maintenance_request_int.change_account(self.account_int)
        self.maintenance_request_int.change_client(self.client_int)
        self.maintenance_request_int.change_instrument(self.eur_gbp)
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
        self.rest_api_ah_msg_2.find_all_auto_hedger()
        self.ah_params_2 = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_2)
        self.ah_params_2 = self.rest_api_manager.parse_response_details(self.ah_params_2,
                                                                        {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params_2["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == 'EUR/GBP':
                i["holdOrder"] = "true"
        self.rest_api_ah_msg_2.clear_message_params().modify_auto_hedger().set_params(self.ah_params_2)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_2)
        self.sleep(3)
        # region Step 3

        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"AccountGroupID": self.client_ext,
                                                                                 "ListingID": self.listing_eur_gbp})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id_ext = self.trade_request.get_exec_id(response)
        ah_order_id = self.trade_request.get_ord_id_from_held(response)
        # self.sleep(3)

        # endregion
        # region Step 4
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
        # region Step 5
        self.ack_request.set_default_ack(ah_order_id)
        self.java_api_manager.send_message(self.ack_request)
        self.sleep(5)

        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameter("ClOrdID", ah_order_id)
        self.ah_exec_report.change_parameter("Account", self.account_int)
        ah_params = ["ClOrdID", "OrdStatus", "ExecType"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report, key_parameters=ah_params, message_name=
        "Check AutoHedger ExecutionReport")

        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "5")
        self.position_report_ext.change_parameter("LastPositUpdateEventID", exec_id_ext)
        self.fix_pos_verifier.check_fix_message(self.position_report_ext,
                                                message_name=f"Check position for {self.client_ext} after order")
        self.position_verifier.check_base_position(external_report, "1000000", text=f"Check base for {self.client_ext}")
        self.sleep(1)
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)
        #
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        internal_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_int,
                                                                                   self.test_id)
        self.position_report_int.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "5")
        self.fix_pos_verifier.check_fix_message(self.position_report_int,
                                                message_name=f"Check position for {self.client_int} after order")
        self.position_verifier.check_base_position(internal_report, "0",
                                                   text=f"Check base for {self.client_int}")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # endregion

        # region Step 6
        self.rest_api_ah_msg_3.find_all_auto_hedger()
        self.ah_params_3 = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_3)
        self.ah_params_3 = self.rest_api_manager.parse_response_details(self.ah_params_3,
                                                                        {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params_3["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == 'EUR/GBP':
                i["holdOrder"] = "false"

        self.rest_api_ah_msg_3.clear_message_params().modify_auto_hedger().set_params(self.ah_params_3)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_3)
        self.sleep(3)
        # endregion

        # region Step 7
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"AccountGroupID": self.client_ext,
                                                                                 "ListingID": self.listing_eur_gbp})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_order_id = self.trade_request.get_ah_ord_id(response)

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
        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameter("ClOrdID", ah_order_id)
        self.ah_exec_report.change_parameter("Account", self.account_int)
        ah_params = ["ClOrdID", "OrdStatus", "ExecType"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report, key_parameters=ah_params, message_name=
        "Check AutoHedger ExecutionReport")
        # endregion
