import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
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


class QAP_T10229(TestCase):
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
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        best_bid = "10"
        best_ask = "11"
        last_trd_px = "10.4"
        size = "200"
        spread = "0.1"
        # region Precondition
        md_req_id = self.market_data_refresh.get_MDReqID(self.listing_id, self.fix_env.feed_handler)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "1", best_ask, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "0", best_bid, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "2", last_trd_px, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.listing_quote.set_default(self.listing_id, quoting_px_ref_type="LTP", spread_px_type="PRC",
                                       bid_spread=spread, offer_spead=spread)
        self.java_api_manager.send_message_and_receive_response(self.listing_quote)
        # endregion
        # region Step 1
        bid_px = str(float(last_trd_px) - float(spread))
        offer_px = str(float(last_trd_px) + float(spread))
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, th_px=str(float(last_trd_px)))
        self.quote_request.change_parameter("REPLY_SUBJECT","_INBOX.TH2.CONNECT.JavaApiUser")
        self.java_api_manager.send_message_and_receive_response(self.quote_request)
        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteManagementReply.value).get_parameters(
        )["MessageReply"]['MessageReplyBlock'][0]
        self.java_api_manager.compare_values({"ErrorMsg": "bid and offer sizes not available"}, quote_rep, "Step 1-2")
        # endregion
