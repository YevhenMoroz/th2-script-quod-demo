from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiQuotingSessionMessages import RestApiQuotingSessionMessages


class QAP_T2480(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.modify_quoting_session = RestApiQuotingSessionMessages()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.quote_4 = FixMessageQuoteFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.currency_gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        self.msg_prams = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        # region MarketData
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_esp = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.gbp_usd_spot = {
            'Symbol': self.gbp_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.gbp_usd_spot,
            'SettlType': self.settle_type_spot}]
        self.md_req_id = "GBP/USD:SPO:REG:HSBC"
        self.bid_px_0 = "1.18060"
        self.offer_px_0 = "1.1813"
        self.no_md_entries_0 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_px_0,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_0,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.bid_px_1 = "1.18079"
        self.offer_px_1 = "1.1814"
        self.no_md_entries_1 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_px_1,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_1,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.bid_px_2 = "1.17079"
        self.offer_px_2 = "1.1714"
        self.no_md_entries_2 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_px_2,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_2,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.bid_px_3 = "1.16079"
        self.offer_px_3 = "1.1614"
        self.no_md_entries_3 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_px_3,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_3,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.bid_px_4 = "1.15079"
        self.offer_px_4 = "1.1514"
        self.no_md_entries_4 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_px_4,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_px_4,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spo,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Setup interval through RestAPI
        self.modify_quoting_session.set_default_params_rfq()
        self.modify_quoting_session.update_parameters({"updateInterval": 10000, "concurrentlyActiveQuoteAge": 120000})
        self.rest_manager.send_post_request(self.modify_quoting_session)
        self.sleep(5)
        # endregion
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_esp.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_esp.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_0)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency_gbp,
                                                           Instrument=self.instrument)
        self.quote_request.remove_fields_in_repeating_group("NoRelatedSymbols", ["Side"])
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        # endregion
        # region Step 3
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_1)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_2)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_3)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_4)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(15)
        # endregion
        # region Step 4
        self.quote_4.set_params_for_quote(self.quote_request)
        self.quote_4.change_parameters({"BidPx": self.bid_px_4, "OfferPx": self.offer_px_4})
        prefilter = {
            "header": {
                "MsgType": ("S", "EQUAL"),
                "TargetCompID": "QUOD9",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["BidPx", "OfferPx", "QuoteReqID"]
        self.fix_verifier.check_fix_message_sequence([self.quote, self.quote_4],
                                                     key_parameters_list=[key_params, key_params],
                                                     pre_filter=prefilter, message_name="Check 2 Quotes")
        # endregion
        # region Step 5
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0], side="1", price=self.offer_px_0)
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.modify_quoting_session.set_default_params_rfq()
        self.rest_manager.send_post_request(self.modify_quoting_session)
        self.sleep(3)
