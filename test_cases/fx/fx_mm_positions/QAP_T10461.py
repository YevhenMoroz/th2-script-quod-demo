from pathlib import Path
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
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX


class QAP_T10461(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier_gtw = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.pos_req_ack = FixMessageRequestForPositionsAckFX()
        self.position_report = FixMessagePositionReportFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.account = self.data_set.get_account_by_name("account_mm_3")
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.usd_php = self.data_set.get_symbol_by_name("symbol_ndf_1")
        self.sec_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date = self.data_set.get_settle_date_by_name("spo_ndf")
        self.instrument = {
            "SecurityType": self.sec_type,
            "Symbol": self.usd_php
        }
        self.instrument_pos = {
            "SecurityType": self.sec_type,
            "Symbol": self.usd_php
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send Trade to have position
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.quote_request.set_rfq_params_ndf()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument,
                                                           SettlDate=self.settle_date)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)

        self.quote.set_params_for_quote_ndf(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single_ndf(self.new_order_single)
        self.execution_report.update_fields_in_component("Instrument", dict(Product="4"))
        self.execution_report.remove_fields_from_component("Instrument", ["MaturityDate"])
        self.fix_verifier_gtw.check_fix_message(self.execution_report)
        exec_id = response[-1].get_parameters()["ExecID"]
        self.sleep(3)
        # endregion
        # region Step 1
        self.request_for_position.set_params_for_ndf()
        self.request_for_position.change_parameters({"Instrument": self.instrument_pos, "Currency": self.currency,
                                                     "Account": self.client})
        self.request_for_position.remove_parameter("SettlDate")
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        # endregion
        # region Step 2
        self.pos_req_ack.set_params_from_reqeust(self.request_for_position)
        self.pos_req_ack.change_parameter("PosReqResult", "0")
        self.fix_verifier.check_fix_message(self.pos_req_ack)
        # endregion
        # region Step 3
        self.position_report.set_params_from_reqeust_ndf(self.request_for_position)
        self.position_report.change_parameter("LastPositUpdateEventID", exec_id)
        self.position_report.remove_fields_from_component("Instrument", ["MaturityDate"])

        self.fix_verifier.check_fix_message(self.position_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
