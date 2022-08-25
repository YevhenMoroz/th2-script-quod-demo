# import logging
# import time
# from datetime import datetime
#
# from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
#
# from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
# from pathlib import Path
#
# from custom.tenor_settlement_date import spo
# from stubs import Stubs
# from th2_grpc_common.common_pb2 import ConnectionID
# from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
#
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# simulator = Stubs.simulator
# act = Stubs.fix_act
# verifier = Stubs.verifier
# api = Stubs.api_service
#
#
# def change_update_interval(case_id, interval):
#     params = {
#         "clientQuoteIDFormat": "#20d",
#         "updateMDEntryID": "true",
#         "ackOrder": "false",
#         "MDUpdateType": "FUL",
#         "quotingSessionName": "QSRFQTH2",
#         "supportMDRequest": "true",
#         "tradingQuotingSession": "true",
#         "quotingSessionID": 10,
#         "concurrentlyActiveQuoteAge": 120000,
#         "updateInterval": interval,
#     }
#     api.sendMessage(
#         request=SubmitMessageRequest(message=bca.wrap_message(params, 'ModifyQuotingSession', 'rest_wa314luna'),
#                                      parent_event_id=case_id))
#
#
# def send_md(case_id, bid_price, ask_price):
#     mdu_params = {
#         "MDReqID": simulator.getMDRefIDForConnection314(
#             request=RequestMDRefID(
#                 symbol="GBP/USD:SPO:REG:HSBC",
#                 connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
#         'Instrument': {
#             'Symbol': 'GBP/USD',
#             'SecurityType': 'FXSPOT'
#         },
#         "NoMDEntries": [
#             {
#                 "MDEntryType": "0",
#                 "MDEntryPx": bid_price,
#                 "MDEntrySize": 1000000,
#                 "MDEntryPositionNo": 1,
#                 "MDQuoteType": 1,
#                 'SettlDate': spo(),
#                 "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
#             },
#             {
#                 "MDEntryType": "1",
#                 "MDEntryPx": ask_price,
#                 "MDEntrySize": 1000000,
#                 "MDEntryPositionNo": 1,
#                 "MDQuoteType": 1,
#                 'SettlDate': spo(),
#                 "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
#             },
#         ]
#     }
#     act.sendMessage(
#         bca.convert_to_request(
#             'Send Market Data SPOT',
#             'fix-fh-314-luna',
#             case_id,
#             bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params, "fix-fh-314-luna")
#         ))
#
#
# def execute(report_id):
#     case_name = Path(__file__).name[:-3]
#     case_id = bca.create_event(case_name, report_id)
#
#     base_bid = 1.18579
#     base_ask = 1.18640
#
#     first_bid = 1.18079
#     first_ask = 1.18140
#
#     second_bid = 1.17079
#     second_ask = 1.17140
#
#     third_bid = 1.16079
#     third_ask = 1.16140
#
#     fourth_bid = 1.15079
#     fourth_ask = 1.15140
#     client_tier = "Iridium1"
#
#     symbol = "GBP/USD"
#     security_type_spo = "FXSPOT"
#     settle_date_spo = spo()
#     settle_type_spo = "0"
#     currency = "GBP"
#
#     qty = "1000000"
#
#     quote_params_base = {
#         'QuoteID': "*",
#         'QuoteMsgID': "*",
#         'BidSpotRate': base_bid,
#         'SettlType': "*",
#         'SettlDate': settle_date_spo,
#         'OfferPx': base_ask,
#         'OfferSize': qty,
#         'BidPx': base_bid,
#         'BidSize': qty,
#         'ValidUntilTime': '*',
#         'OfferSpotRate': base_ask,
#         'Currency': currency,
#         'Instrument': {
#             'Symbol': symbol,
#             'SecurityType': security_type_spo,
#             'Product': 4,
#         },
#         'QuoteReqID': '*',
#         'QuoteType': 1,
#     }
#     quote_params4 = {
#         'QuoteID': "*",
#         'QuoteMsgID': "*",
#         'BidSpotRate': fourth_bid,
#         'SettlType': "*",
#         'SettlDate': settle_date_spo,
#         'OfferPx': fourth_ask,
#         'OfferSize': qty,
#         'BidPx': fourth_bid,
#         'BidSize': qty,
#         'ValidUntilTime': '*',
#         'OfferSpotRate': fourth_ask,
#         'Currency': currency,
#         'Instrument': {
#             'Symbol': symbol,
#             'SecurityType': security_type_spo,
#             'Product': 4,
#         },
#         'QuoteReqID': '*',
#         'QuoteType': 1,
#     }
#
#     try:
#         change_update_interval(case_id, 10000)
#         send_md(case_id, base_bid, base_ask)
#         time.sleep(5)
#         checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
#         checkpoint_id = checkpoint_response.checkpoint
#         quote_req_id = bca.client_orderid(8)
#         quote_request_params = {
#             'QuoteReqID': quote_req_id,
#             'NoRelatedSymbols': [{
#                 'Account': client_tier,
#                 'Instrument': {
#                     'Symbol': symbol,
#                     'SecurityType': security_type_spo
#                 },
#                 'SettlDate': settle_date_spo,
#                 'SettlType': settle_type_spo,
#                 'Currency': currency,
#                 'QuoteType': '1',
#                 'OrderQty': qty,
#                 'OrdType': 'D'
#             }
#             ]
#         }
#         quote = act.placeQuoteFIX(
#             request=bca.convert_to_request(
#                 "SendQuoteRequest",
#                 "fix-ss-rfq-314-luna-standard",
#                 case_id,
#                 bca.message_to_grpc("QuoteRequest", quote_request_params, "fix-ss-rfq-314-luna-standard")
#             )
#         )
#         send_md(case_id, first_bid, first_ask)
#         time.sleep(1)
#         send_md(case_id, second_bid, second_ask)
#         time.sleep(1)
#         send_md(case_id, third_bid, third_ask)
#         time.sleep(1)
#         send_md(case_id, fourth_bid, fourth_ask)
#         time.sleep(10)
#         quotes_sequence_params = {
#             'header': {
#                 'MsgType': ('0', "NOT_EQUAL"),
#                 'TargetCompID': 'QUOD9',
#                 'SenderCompID': 'QUODFX_UAT'
#             },
#         }
#         message_filters_req = [
#             bca.filter_to_grpc('Quote', quote_params_base),
#             bca.filter_to_grpc('Quote', quote_params4)
#         ]
#         pre_filter_req = bca.prefilter_to_grpc(quotes_sequence_params)
#         verifier.submitCheckSequenceRule(
#             bca.create_check_sequence_rule(
#                 description="Check Quotes",
#                 prefilter=pre_filter_req,
#                 msg_filters=message_filters_req,
#                 checkpoint=checkpoint_id,
#                 connectivity="fix-ss-rfq-314-luna-standard",
#                 event_id=case_id,
#                 timeout=3000
#             )
#         )
#         quote_req_id = quote.response_messages_list[0].fields["QuoteReqID"].simple_value
#         quote_cancel_params = {
#             'QuoteReqID': quote_req_id,
#             'QuoteID': '*',
#             'QuoteCancelType': '5',
#         }
#         act.sendMessage(
#             bca.convert_to_request(
#                 'Send QuoteCancel', "fix-ss-rfq-314-luna-standard", case_id,
#                 bca.message_to_grpc('QuoteCancel', quote_cancel_params,
#                                     "fix-ss-rfq-314-luna-standard")
#             ))
#         change_update_interval(case_id, 10000)
#     except Exception:
#         logging.error('Error execution', exc_info=True)

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
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiQuotingSessionMessages import RestApiQuotingSessionMessages


class QAP_T2528(TestCase):
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
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.modify_quoting_session = RestApiQuotingSessionMessages()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.quote_1 = FixMessageQuoteFX()
        self.quote_2 = FixMessageQuoteFX()
        self.quote_3 = FixMessageQuoteFX()
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
        self.md_req_id = "GBP/USD:SPO:REG:HSBC"
        self.bid_px_0 = "1.16079"
        self.offer_px_0 = "1.1614"
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
        self.modify_quoting_session.update_parameters({"updateInterval": 10000})
        self.rest_manager.send_post_request(self.modify_quoting_session)
        self.sleep(5)
        # endregion
        # region Step 1
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
        self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.quote.change_parameters({"BidPx": self.bid_px_0, "OfferPx": self.offer_px_0})
        # endregion
        # region Step 3
        self.sleep(10)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_1)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(1)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_2)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(1)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_3)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_4)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(10)
        # endregion
        # region Step 4
        self.quote_1.set_params_for_quote(self.quote_request)
        self.quote_1.change_parameters({"BidPx": self.bid_px_1, "OfferPx": self.offer_px_1})
        self.quote_2.set_params_for_quote(self.quote_request)
        self.quote_2.change_parameters({"BidPx": self.bid_px_2, "OfferPx": self.offer_px_2})
        self.quote_3.set_params_for_quote(self.quote_request)
        self.quote_3.change_parameters({"BidPx": self.bid_px_3, "OfferPx": self.offer_px_3})
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
        self.fix_verifier.check_fix_message_sequence(
            [self.quote,self.quote_1, self.quote_4],
            key_parameters_list=[key_params, key_params, key_params],
            pre_filter=prefilter, message_name="Check 4 Quotes")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.quote_cancel.set_params_for_cancel(self.quote_request)
        self.fix_manager_gtw.send_message(self.quote_cancel)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.modify_quoting_session.set_default_params_rfq()
        self.modify_quoting_session.update_parameters({"updateInterval": 12000})
        self.rest_manager.send_post_request(self.modify_quoting_session)
        self.sleep(3)
