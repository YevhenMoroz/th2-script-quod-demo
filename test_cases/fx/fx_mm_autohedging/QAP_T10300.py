from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.fix_wrappers.forex.FixMessageOrderCancelReplaceRequestFX import \
    FixMessageOrderCancelReplaceRequestFX
from test_framework.fix_wrappers.forex.FixMessageOrderCancelRequestFX import FixMessageOrderCancelRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.JavaApiVerifier import JavaApiVerifier
from test_framework.java_api_wrappers.aqs_messages.AutoHedgerInstrSymbolStatusManagementRequest import \
    AutoHedgerInstrSymbolStatusManagementRequest
from test_framework.java_api_wrappers.aqs_messages.AutoHedgerStatusManagementRequest import \
    AutoHedgerStatusManagementRequest
from test_framework.java_api_wrappers.fx.AutoHedgerInstrSymbolBatchUpdateFX import AutoHedgerInstrSymbolBatchUpdateFX
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiAutoHedgerMessages import RestApiAutoHedgerMessages


class QAP_T10300(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.java_api_verifier = JavaApiVerifier(self.java_api_env, self.test_id)
        self.rest_api_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.ah_update = AutoHedgerInstrSymbolBatchUpdateFX()
        self.ah_status_web = RestApiAutoHedgerMessages()
        self.ah_status = AutoHedgerInstrSymbolStatusManagementRequest()
        self.ah_status_fe = AutoHedgerStatusManagementRequest()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_jpy = self.data_set.get_symbol_by_name("symbol_4")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.ja_date = self.data_set.get_settle_date_by_name("spot_java_api")
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.ah_id = self.data_set.get_auto_hedger_id_by_name("auto_hedger_id_1")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_jpy
        }
        self.qty = "30000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position start
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # endregion

        # region Step 2
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext, "ExecQty": self.qty,
                                                       "SettlDate": self.ja_date, "Currency": self.currency})
        self.trade_request.change_instrument(self.eur_jpy, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region Step 3
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters({"Account": self.client_int,
                                         "SettlDate": self.settle_date, "OrderQty": self.qty})
        self.ah_order.remove_parameters(["Misc0"])
        self.sleep(20)
        prefilter = {
            "header": {
                "MsgType": ("D", "EQUAL"),
                "TargetCompID": "QUOD8",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["Account", "OrderQty"]
        msg_list = [self.ah_order, self.ah_order, self.ah_order, self.ah_order, self.ah_order]
        key_params_list = [key_params, key_params, key_params, key_params, key_params]
        self.fix_drop_copy_verifier.check_fix_message_sequence(fix_messages_list=msg_list,
                                                               key_parameters_list=key_params_list,
                                                               pre_filter=prefilter)
        # TODO update params for self.ah_update
        self.ah_update.set_default_params(self.ah_id, self.eur_jpy)
        self.java_api_verifier.check_java_message(self.ah_update)
        # endregion
        # region Step 4
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.ah_status.set_default(self.ah_id, self.eur_jpy, "Y")
        self.java_api_manager.send_message(self.ah_status)
        self.sleep(10)
        msg = "Check new 5 AH orders"
        self.fix_drop_copy_verifier.check_fix_message_sequence(fix_messages_list=msg_list,
                                                               key_parameters_list=key_params_list,
                                                               pre_filter=prefilter,
                                                               message_name=msg)
        # TODO update params for self.ah_update
        self.ah_update.set_default_params(self.ah_id, self.eur_jpy)
        self.java_api_verifier.check_java_message(self.ah_update)
        # endregion

        # region Step 5
        self.sleep(15)
        self.ah_status_web.send_hedge_orders_false()
        self.rest_api_manager.send_post_request(self.ah_status_web)
        self.sleep(5)
        self.ah_status_web.send_hedge_orders_true()
        self.rest_api_manager.send_post_request(self.ah_status_web)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.sleep(10)
        self.fix_drop_copy_verifier.check_fix_message_sequence(fix_messages_list=msg_list,
                                                               key_parameters_list=key_params_list,
                                                               pre_filter=prefilter,
                                                               message_name=msg)
        # TODO update params for self.ah_update
        self.ah_update.set_default_params(self.ah_id, self.eur_jpy)
        self.java_api_verifier.check_java_message(self.ah_update)
        # endregion

        # region Step 6
        self.sleep(15)
        self.ah_status_fe.send_hedge_orders_false()
        self.java_api_manager.send_message(self.ah_status_fe)
        self.sleep(5)
        self.ah_status_fe.send_hedge_orders_true()
        self.java_api_manager.send_message(self.ah_status_fe)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.sleep(10)
        self.fix_drop_copy_verifier.check_fix_message_sequence(fix_messages_list=msg_list,
                                                               key_parameters_list=key_params_list,
                                                               pre_filter=prefilter,
                                                               message_name=msg)
        # TODO update params for self.ah_update
        self.ah_update.set_default_params(self.ah_id, self.eur_jpy)
        self.java_api_verifier.check_java_message(self.ah_update)
        self.sleep(5)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.ah_status.set_default(self.ah_id, self.eur_jpy, "Y")
        self.java_api_manager.send_message(self.ah_status)
