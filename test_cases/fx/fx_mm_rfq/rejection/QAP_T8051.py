from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiModifyMarketMakingStatusMessages import \
    RestApiModifyMarketMakingStatusMessages


class QAP_T8051(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.modify_mm_status = RestApiModifyMarketMakingStatusMessages()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.currency_gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.msg_prams = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_req_id = "GBP/USD:SPO:REG:HSBC"
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        # self.quote_request.set_rfq_params()
        # self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
        #                                                    Account=self.client,
        #                                                    Currency=self.currency_gbp,
        #                                                    Instrument=self.instrument)
        # response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        # self.quote.set_params_for_quote(self.quote_request)
        # self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 2
        self.modify_mm_status.set_default_params().set_executable_disable()
        self.rest_manager.send_post_request(self.modify_mm_status)
        # TODO check test case
        # self.sleep(5)
        # self.fix_md.set_market_data()
        # self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        # self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        # # endregion
        # # region Step 3
        # self.quote_request.set_rfq_params()
        # self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
        #                                                    Account=self.client,
        #                                                    Currency=self.currency_gbp,
        #                                                    Instrument=self.instrument)
        # self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        # self.quote.set_params_for_quote(self.quote_request)
        # self.fix_verifier.check_fix_message(self.quote)
        # endregion
    #
    #
    # @try_except(test_id=Path(__file__).name[:-3])
    # def run_post_conditions(self):
    #     self.modify_mm_status.set_default_params().set_executable_enable()
    #     self.rest_manager.send_post_request(self.modify_mm_status)
