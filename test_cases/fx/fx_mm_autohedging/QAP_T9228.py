from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportDropCopyFX import FixMessageExecutionReportDropCopyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.HeldOrderAckRequestFX import HeldOrderAckRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiAutoHedgerMessages import RestApiAutoHedgerMessages


class QAP_T9228(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.rest_api_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
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
        self.exec_qty = "1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rest_api_ah_msg_1.find_all_auto_hedger()
        self.ah_params = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_1)
        self.ah_params = self.rest_api_manager.parse_response_details(self.ah_params,
                                                                      {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == self.eur_gbp:
                i["holdOrder"] = "true"
        self.rest_api_ah_msg_1.clear_message_params().modify_auto_hedger().set_params(self.ah_params)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_1)
        self.sleep(3)
        # endregion
        # region Step 2
        self.trade_request.set_default_params()
        self.trade_request.remove_fields_from_component("TradeEntryRequestBlock", ["SettlDate"])
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext,
                                                       "ExecQty": self.exec_qty})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_order_id = self.trade_request.get_ord_id_from_held(response)

        # endregion
        # region Step 3-4
        self.ack_request.set_default_ack(ah_order_id)
        self.java_api_manager.send_message(self.ack_request)
        self.sleep(1)
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
                                                               message_name="Check that we create AH order")
        self.sleep(5)
        # endregion
        # region Step 5
        self.trade_request.set_default_params()
        self.trade_request.remove_fields_from_component("TradeEntryRequestBlock", ["SettlDate"])
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext,
                                                       "ExecQty": self.exec_qty})
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_order_id = self.trade_request.get_ord_id_from_held(response)

        # endregion
        # region Step6
        self.ack_request.set_default_rej(ah_order_id)
        self.java_api_manager.send_message(self.ack_request)
        self.sleep(1)
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters({"Account": self.client_int, "ClOrdID": ah_order_id})
        key_params = ["Misc0", "Account"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order, key_parameters=key_params,
                                                      message_name="Check that we create AH order")

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_ah_msg_2.find_all_auto_hedger()
        self.ah_params_2 = self.rest_api_manager.send_get_request_filtered(self.rest_api_ah_msg_2)
        self.ah_params_2 = self.rest_api_manager.parse_response_details(self.ah_params_2,
                                                                        {"autoHedgerName": self.auto_hedger_name})
        for i in self.ah_params_2["autoHedgerInstrSymbol"]:
            if i["instrSymbol"] == self.eur_gbp:
                i["holdOrder"] = "false"

        self.rest_api_ah_msg_2.clear_message_params().modify_auto_hedger().set_params(self.ah_params_2)
        self.rest_api_manager.send_post_request(self.rest_api_ah_msg_2)
        self.sleep(3)
