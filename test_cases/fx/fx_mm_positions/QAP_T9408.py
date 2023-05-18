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


class QAP_T9408(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.maintenance_request = FixPositionMaintenanceRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier_gtw = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_report = FixMessagePositionReportFX()
        self.position_report_2 = FixMessagePositionReportFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.listing_gbp_cad_wk1 = self.data_set.get_listing_id_by_name("gbp_cad_wk1")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.sec_type_java = self.data_set.get_fx_instr_type_ja("fx_fwd")
        self.instrument = {
            "SecurityType": self.sec_type_fwd,
            "Symbol": self.gbp_cad
        }
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1_java_api")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)

        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier_gtw.check_fix_message(self.execution_report)
        exec_id = response[0].get_parameters()["ExecID"]
        self.sleep(3)
        # endregion
        # region Step 2
        self.request_for_position.set_params_for_fwd()
        self.request_for_position.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                     "Account": self.client})
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)

        self.maintenance_request.set_params_for_fwd()
        self.maintenance_request.change_account(self.account)
        self.maintenance_request.change_client(self.client)
        self.maintenance_request.change_instrument(self.gbp_cad, self.sec_type_java)
        self.java_api_manager.send_message(self.maintenance_request)
        self.sleep(1)
        # endregion
        # region Step 3
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("LastPositUpdateEventID", exec_id)
        self.position_report_2.set_params_from_reqeust(self.request_for_position)
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
