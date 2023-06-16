from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX


class QAP_T2855(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_verifier_gtw = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.pos_report_none = FixMessageRequestForPositionsAckFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.quote = FixMessageQuoteFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.qty = "3000000"
        self.instrument = {
            "SecurityType": self.sec_type_fwd,
            "Symbol": self.eur_usd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check that they equal to 0
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)

        self.request_for_position_ext.set_params_for_fwd()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_ext, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_ext)
        self.fix_verifier.check_fix_message(self.pos_report_none,
                                            message_name=f"Check position for {self.client_ext} before start")
        self.sleep(1)
        self.request_for_position_ext.set_params_for_fwd()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)

        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_int)
        self.fix_verifier.check_fix_message(self.pos_report_none,
                                            message_name=f"Check position for {self.client_int} before start")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)

        # endregion
        # region Step 1
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client_ext,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument,
                                                           OrderQty=self.qty)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        # endregion
        # region Step 2
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier_gtw.check_fix_message(self.execution_report)
        # endregion
        # region Step 3
        self.ah_order.set_default_from_request(self.quote_request)
        self.ah_order.change_parameter("Account", self.client_int)
        ah_params = ["Account", "OrderQty"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order, key_parameters=ah_params,
                                                      message_name="Check AutoHedger Order on DropCopy gtw")
        # endregion
