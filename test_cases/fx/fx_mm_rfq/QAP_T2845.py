from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2845(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.rest_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.execution_report_fill = FixMessageExecutionReportPrevQuotedFX()
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.rest_manager = RestApiManager(self.rest_env, self.test_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.clint_tier_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.status = Status.Reject
        self.md_req_id = "GBP/USD:FXF:WK1:HSBC"
        self.offer_px_1 = 1.18155
        self.offer_px_2 = 1.18165
        self.no_md_entries_wk1_1 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18145,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_1,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": "0.00002",
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }]
        self.no_md_entries_wk1_2 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18145,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_2,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00003",
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send MD
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_wk1_1)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region Step 1
        self.rest_massage.find_all_client_tier_instrument()
        params_eur_usd = self.rest_manager.send_get_request(self.rest_massage)
        params_eur_usd = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {"clientTierID": self.clint_tier_id, "instrSymbol": self.gbp_usd})
        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_eur_usd). \
            update_value_in_component("clientTierInstrSymbolTenor", "validatePriceSlippage", "true",
                                      {"tenor": "WK1"})
        self.rest_massage.update_value_in_component("clientTierInstrSymbolTenor", "priceSlippageRange", "1",
                                                    {"tenor": "WK1"})
        self.rest_manager.send_post_request(self.rest_massage)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           Account=self.account,
                                                           Instrument=self.instrument,
                                                           Currency=self.currency)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        price = response[0].get_parameter("OfferPx")
        range_above = str(round(float(price) + 0.00011, 5))
        range_bellow = str(round(float(price) - 0.00009, 5))
        price_above = str(float(price) + 0.0003)
        # endregion
        #
        # region Step 3
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_wk1_2)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region Step 4
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.new_order_single.change_parameter("Price", price_above)
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, status=self.status,
                                                               text=f"invalid price")
        self.fix_verifier_sell.check_fix_message(self.execution_report)
        # endregion
        # region Step 5
        self.execution_report.set_params_from_new_order_single(self.new_order_single, status=self.status,
                                                               text=f"order price is not ranging in [{range_bellow}, "
                                                                    f"{range_above}]")
        self.fix_verifier_dc.check_fix_message(self.execution_report)
        # endregion
        # region Step 6
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.new_order_single.change_parameter("Price", price)
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report_fill.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier_sell.check_fix_message(self.execution_report_fill)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.rest_massage.update_value_in_component("clientTierInstrSymbolTenor", "validatePriceSlippage", "false",
                                                    {"tenor": "WK1"})
        self.rest_manager.send_post_request(self.rest_massage)
