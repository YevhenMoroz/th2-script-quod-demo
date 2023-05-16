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
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T11222(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.rfq_connectivity, self.test_id)
        self.fix_manager_pks = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.rfq_connectivity, self.test_id)
        self.fix_verifier_pks = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.pos_report = FixMessageRequestForPositionsAckFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.trade_request = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_9")
        self.account = self.data_set.get_account_by_name("account_mm_9")

        self.currency_eur = self.data_set.get_currency_by_name("currency_eur")
        self.currency_gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_wk1_java = self.data_set.get_settle_date_by_name("spot_java_api")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("spot")
        self.instrument_fwd = {
            "SecurityType": self.sec_type_fwd,
            "Symbol": self.eur_usd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency_eur,
                                                           Instrument=self.instrument_fwd)
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)

        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.eur_usd, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region Step 2
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(3)
        # endregion
        self.request_for_position.set_params_for_all()

        # region Step 3
        self.request_for_position.change_parameter("Account", self.client)
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position)
        # endregion

        # region Step 4
        self.pos_report.set_params_for_none(self.request_for_position)
        self.fix_verifier_pks.check_fix_message(self.pos_report)
        # endregion

        # region Step 5
        self.request_for_position.set_unsubscribe()
        self.fix_manager_pks.send_message(self.request_for_position)
        # endregion

        # region Step 6
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.gbp_cad, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)

        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client})
        self.trade_request.change_instrument(self.eur_usd, self.instr_type_spo)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region Step 7
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(3)
        self.request_for_position.set_params_for_all()
        self.request_for_position.change_parameter("Account", self.client)
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position)
        self.pos_report.set_params_for_none(self.request_for_position)
        self.fix_verifier_pks.check_fix_message(self.pos_report)
        self.request_for_position.set_unsubscribe()
        self.fix_manager_pks.send_message(self.request_for_position)
        # endregion
