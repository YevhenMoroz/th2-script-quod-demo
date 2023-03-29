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
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T2934(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.maintenance_request_ext = FixPositionMaintenanceRequestFX()
        self.maintenance_request_int = FixPositionMaintenanceRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_verifier_gtw = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.position_verifier = PositionVerifier(self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.position_report_ext = FixMessagePositionReportFX()
        self.position_report_int = FixMessagePositionReportFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_7")
        self.account_ext = self.data_set.get_account_by_name("account_mm_7")
        self.client_int = self.data_set.get_client_by_name("client_int_4")
        self.account_int = self.data_set.get_account_by_name("account_int_4")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.gbp_cad
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check that they equal to 0
        self.maintenance_request_ext.set_default_params()
        self.maintenance_request_ext.change_account(self.account_ext)
        self.maintenance_request_ext.change_client(self.client_ext)
        self.maintenance_request_ext.change_instrument(self.gbp_cad)
        self.java_api_manager.send_message(self.maintenance_request_ext)
        self.sleep(1)
        self.maintenance_request_int.set_default_params()
        self.maintenance_request_int.change_account(self.account_int)
        self.maintenance_request_int.change_client(self.client_int)
        self.maintenance_request_int.change_instrument(self.gbp_cad)
        self.java_api_manager.send_message(self.maintenance_request_int)
        self.sleep(1)

        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "11")
        self.fix_verifier.check_fix_message(self.position_report_ext,
                                            message_name=f"Check position for {self.client_ext} before start")
        self.position_verifier.check_base_position(external_report, "0")
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
        self.fix_verifier.check_fix_message(self.position_report_int,
                                            message_name=f"Check position for {self.client_int} before start")
        self.position_verifier.check_base_position(internal_report, "0")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)

        # endregion
        # region Step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client_ext,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument,
                                                           Side="2")
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier_gtw.check_fix_message(self.execution_report)
        # endregion
        # region Step 2
        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "5")
        self.fix_verifier.check_fix_message(self.position_report_ext,
                                            message_name=f"Check position for {self.client_ext} after order")
        self.position_verifier.check_base_position(external_report, "-1000000")
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
        self.position_report_int.change_parameter("LastPositEventType", "5")
        self.fix_verifier.check_fix_message(self.position_report_int,
                                            message_name=f"Check position for {self.client_int} after order")
        self.position_verifier.check_base_position(internal_report, "1000000")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # endregion
