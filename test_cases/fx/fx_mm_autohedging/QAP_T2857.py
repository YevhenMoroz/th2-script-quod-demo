from datetime import datetime, timedelta
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
from test_framework.java_api_wrappers.JavaApiVerifier import JavaApiVerifier
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T2857(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.java_api_verifier = JavaApiVerifier(self.java_api_env, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.ja_date = self.data_set.get_settle_date_by_name("spot_java_api")
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.ah_id = self.data_set.get_auto_hedger_id_by_name("auto_hedger_id_1")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_gbp
        }
        self.qty = "30000000"
        self.now = None
        self.start_date = None

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
        self.trade_request.change_instrument(self.eur_gbp, self.instr_type_spo)
        self.now = datetime.utcnow()
        self.start_date = self.now
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_order_id = self.trade_request.get_ah_ord_id(response)
        # endregion

        # region Step 3
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters({"Account": self.client_int, "ClOrdID": ah_order_id, })
        self.ah_order.remove_parameters(["Misc0"])
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order, message_name="Check that we create AH order")
        # endregion

        # region Step 4
        self.sleep(60)
        self.ah_exec_report.set_params_for_cancel(self.trade_request)
        self.ah_exec_report.change_parameters({"OrderID": ah_order_id, "OrigClOrdID": ah_order_id,
                                               "Account": self.client_int})
        self.ah_exec_report.change_parameter("TransactTime",
                                             f">{(self.start_date + timedelta(seconds=60)).isoformat()[:-6]}")
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report, message_name="Check that order is canceled",
                                                      key_parameters=["OrderID", "ExecType", "OrdStatus"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
