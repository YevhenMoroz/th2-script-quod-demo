from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import check_ah_decision
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportDropCopyFX import FixMessageExecutionReportDropCopyFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T2450(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.eur_usd
        }
        self.qty = "3000000"
        self.expected_notes = "open quantity of position (3e+06) exceeds the low watermark (0)"
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

        # region Step 1
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext, "ExecQty": self.qty})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ord_id = self.trade_request.get_ah_ord_id(response)

        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameter("OrderID", ord_id)
        self.ah_exec_report.change_parameter("Account", self.account_int)
        ah_exec_params = ["OrderID", "OrdStatus", "OrderQty"]
        self.sleep(5)
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report,
                                                      key_parameters=ah_exec_params,
                                                      message_name="Check AutoHedger ExecutionReport")
        # endregion
        # region Step 2
        notes = check_ah_decision(ord_id)
        self.verifier.set_event_name("Check AH decision")
        self.verifier.compare_values("Free notes", self.expected_notes, notes)
        self.verifier.verify()
        #