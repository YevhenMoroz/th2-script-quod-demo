import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import QSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageMarketDataIncrementalRefreshOMS import \
    FixMessageMarketDataIncrementalRefreshOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.qs_messages.ListingQuotingModificationRequest import \
    ListingQuotingModificationRequest
from test_framework.java_api_wrappers.qs_messages.QuoteManagementRequest import QuoteManagementRequest
from test_framework.java_api_wrappers.qs_messages.StopQuotingRequest import StopQuotingRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10192(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.listing_quote = ListingQuotingModificationRequest()
        self.quote_request = QuoteManagementRequest()
        self.market_data_refresh = FixMessageMarketDataIncrementalRefreshOMS()
        self.stop_quoting_req = StopQuotingRequest()
        self.listing_id = self.data_set.get_listing_id_by_name("listing_1")
        self.client = self.data_set.get_client_by_name("client_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        best_bid = "10.0"
        best_ask = "11.0"
        size = "200"
        spread = "0.1"
        nat_amt = "5000"
        last_trd_px = "10.4"
        # region Precondition

        md_req_id = self.market_data_refresh.get_MDReqID(self.listing_id, self.fix_env.feed_handler)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "1", best_ask, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "0", best_bid, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "2", last_trd_px, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        # endregion
        # region Step 1
        self.listing_quote.set_default(self.listing_id, quoting_px_ref_type="LTP", spread_px_type="PRC",
                                       bid_spread=spread, offer_spead=spread)
        self.java_api_manager.send_message_and_receive_response(self.listing_quote)
        self.java_api_manager.get_last_message(QSMessageType.ListingQuotingNotification.value)
        # endregion
        # region Step 2
        bid_px = str(float(last_trd_px) - float(spread))
        offer_px = str(float(last_trd_px) + float(spread))
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, notional_amt=nat_amt, th_px=last_trd_px)
        try:
            rej_rule = self.rule_manager.add_NewOrderSingle_ExecutionReport_Reject_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.mic, float(bid_px))
            rej_rule2 = self.rule_manager.add_NewOrderSingle_ExecutionReport_Reject_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.mic, float(offer_px))
            self.java_api_manager.send_message_and_receive_response(self.quote_request)
        except Exception as e:
            logger.error(f"Exception {e} was raised")
        finally:
            self.rule_manager.remove_rules([rej_rule,rej_rule2])
        # endregion
        # region Step 3
        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters(
        )["QuoteStatusReportBlock"]
        exp_res = {"ListingID": self.listing_id, "AccountGroupID": self.client, "ExDestination": self.mic,
                   "Currency": self.currency, "QuoteStatus": "REJ", "BidPx": bid_px, "OfferPx": offer_px}
        self.java_api_manager.compare_values(exp_res, quote_rep, "Step 2-3")
        # endregion
        # region Step 4-6
        self.java_api_manager.send_message_and_receive_response(self.quote_request)
        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters(
        )["QuoteStatusReportBlock"]
        exp_res = {"ListingID": self.listing_id, "AccountGroupID": self.client, "ExDestination": self.mic,
                   "Currency": self.currency, "QuoteStatus": "ACK", "BidPx": bid_px, "OfferPx": offer_px}
        self.java_api_manager.compare_values(exp_res, quote_rep, "Step 4-6")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.stop_quoting_req.set_default(self.listing_id)
        self.java_api_manager.send_message(self.stop_quoting_req)
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")