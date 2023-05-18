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
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T11080(TestCase):
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
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_report_before_spot = FixMessagePositionReportFX()
        self.position_report_before_fwd = FixMessagePositionReportFX()
        self.position_report_after_mo = FixMessagePositionReportFX()
        self.position_report_after_exe = FixMessagePositionReportFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.trade_request = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.listing_gbp_cad = self.data_set.get_listing_id_by_name("gbp_cad_spo")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.sec_type_java = self.data_set.get_fx_instr_type_ja("fx_fwd")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "SecurityType": self.fwd,
            "Symbol": self.gbp_cad
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send Trade to have position
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id_spo = self.trade_request.get_exec_id(response)
        self.sleep(5)
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument,
                                                           Side="2")
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)

        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        exec_id_fwd = response[0].get_parameters()["ExecID"]
        self.sleep(5)
        # endregion
        # region Step 2
        self.request_for_position.set_params_for_all()
        self.request_for_position.change_parameters({"Account": self.client, })
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        # endregion
        # region Step 3
        # TODO add Check RequestForPositionsAck
        # endregion
        # region Step 4
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency,
                                                           Instrument=self.instrument,
                                                           Side="2")
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)

        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        mo_id_after = response[0].get_parameters()["OrderID"]
        exec_id_after = response[0].get_parameters()["ExecID"]
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier_gtw.check_fix_message(self.execution_report)
        # endregion
        # region Step 5
        self.position_report_before_spot.set_params_for_all(self.request_for_position)
        self.position_report_before_spot.change_parameter("LastPositUpdateEventID", exec_id_spo)

        self.position_report_before_fwd.set_params_for_all(self.request_for_position)
        self.position_report_before_fwd.change_parameter("LastPositUpdateEventID", exec_id_fwd)

        self.position_report_after_mo.set_params_for_all(self.request_for_position)
        self.position_report_after_mo.change_parameter("LastPositUpdateEventID", mo_id_after)
        self.position_report_after_exe.set_params_for_all(self.request_for_position)
        self.position_report_after_exe.change_parameter("LastPositUpdateEventID", exec_id_after)
        prefilter = {
            "header": {
                "MsgType": ("AP", "EQUAL"),
                "TargetCompID": "PKSTH2",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["PosReqID"]
        self.sleep(3)
        self.fix_verifier.check_fix_message_sequence([self.position_report_before_spot,
                                                      self.position_report_before_fwd,
                                                      self.position_report_after_mo,
                                                      self.position_report_after_exe],
                                                     key_parameters_list=[key_params, key_params, key_params,
                                                                          key_params],
                                                     pre_filter=prefilter,
                                                     message_name="Check that we receive 4 report ")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
