import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from datetime import timezone
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import QSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageMarketDataIncrementalRefreshOMS import (
    FixMessageMarketDataIncrementalRefreshOMS,
)
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.qs_messages.ListingQuotingModificationRequest import (
    ListingQuotingModificationRequest,
)
from test_framework.java_api_wrappers.qs_messages.QuoteManagementRequest import QuoteManagementRequest
from test_framework.java_api_wrappers.qs_messages.StopQuotingRequest import StopQuotingRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T10258(TestCase):
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
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        best_bid = "10.0"
        best_ask = "11.0"
        size = "200"
        last_trd_px = "10.4"
        spread = "0.1"
        bid_size = "1000.0"
        offer_size = "1000.0"

        # region Precondition
        md_req_id = self.market_data_refresh.get_MDReqID(self.listing_id, self.fix_env.feed_handler)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "0", best_bid, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "1", best_ask, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "2", last_trd_px, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        # endregion

        # region Step 1
        self.listing_quote.set_default(
            self.listing_id, spread_px_type="PRC", bid_spread=spread, offer_spead=spread
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.listing_quote)
        print_message("Check quote setup", responses)
        quot_notify = self.java_api_manager.get_last_message(QSMessageType.ListingQuotingNotification.value)
        exp_res = self.listing_quote.get_parameters()["ListingQuotingModificationRequestBlock"]
        exp_res.update({"QuoteOfferSizeStatus": "COR", "QuoteBidSizeStatus": "COR"})
        self.java_api_manager.compare_values(
            exp_res, quot_notify.get_parameters()["ListingQuotingNotificationBlock"], "Step 1 - Check quote setup"
        )
        # endregion
        # region Step 2
        self.quote_request.set_default(self.listing_id, offer_size, bid_size)
        self.java_api_manager.send_message(self.quote_request)
        result = self.ssh_client.get_regex_pattern(f"/Logs/{self.ssh_client_env.su_user}/QUOD.QS.log",
            "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*bid and offer sizes not available")[-1]
        exp_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        self.java_api_manager.compare_values({"exp_time": exp_time}, {"exp_time": result},
                                             "Step 2 - Check rejected quote", VerificationMethod.CONTAINS)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.stop_quoting_req.set_default(self.listing_id)
        self.java_api_manager.send_message(self.stop_quoting_req)
