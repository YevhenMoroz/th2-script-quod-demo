import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import QSMessageType, ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageMarketDataIncrementalRefreshOMS import (
    FixMessageMarketDataIncrementalRefreshOMS,
)
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.qs_messages.ListingQuotingModificationRequest import (
    ListingQuotingModificationRequest,
)
from test_framework.java_api_wrappers.qs_messages.QuoteManagementRequest import QuoteManagementRequest
from test_framework.java_api_wrappers.qs_messages.StopQuotingRequest import StopQuotingRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T10354(TestCase):
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
        self.rule_manager = RuleManager(Simulators.equity)
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        best_bid = "10.0"
        best_ask = "11.0"
        size = "200"
        last_trd_px = "10.2"
        spread = "1.0"
        bid_size = "1000.0"
        offer_size = "1000.0"

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
        self.listing_quote.set_default(self.listing_id, spread_px_type="PRC", bid_spread=spread, offer_spead=spread)
        self.java_api_manager.send_message(self.listing_quote)

        bid_px: str = str(float(last_trd_px) - float(spread))
        offer_px: str = str(float(last_trd_px) + float(spread))
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, offer_size, bid_size)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(bid_px))
            nos_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(offer_px))
            self.java_api_manager.send_message_and_receive_response(self.quote_request)
        except Exception as e:
            logger.error(f'Your Exception is {e}')
            # endregion
        finally:
            time.sleep(3)
            self.rule_manager.remove_rules([nos_rule, nos_rule2])
        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters()[
            "QuoteStatusReportBlock"
        ]
        ord_id = quote_rep["SimulatingOrderList"]["SimulatingOrderBlock"][0]["OrdID"]
        ord_id2 = quote_rep["SimulatingOrderList"]["SimulatingOrderBlock"][1]["OrdID"]

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value
        ]
        exp_res = {"OrdQty": bid_size, "Price": bid_px, "Side": "B"}
        self.java_api_manager.compare_values(exp_res, ord_rep, "Step 1 - Check created order 1")

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id2
                                                         ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        exp_res = {"OrdQty": offer_size, "Price": offer_px, "Side": "S"}
        self.java_api_manager.compare_values(exp_res, ord_rep, "Step 1 - Check created order 2")
        # endregion
        # region Step 2
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, offer_size, bid_size, side="S")
        try:
            cr_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, True)
            self.java_api_manager.send_message_and_receive_response(self.quote_request)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cr_rule)
        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters()[
            "QuoteStatusReportBlock"
        ]
        ord_id = quote_rep["SimulatingOrderList"]["SimulatingOrderBlock"][0]["OrdID"]
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        exp_res = {"OrdQty": bid_size, "Price": bid_px, "Side": "B", "TransStatus": "CXL"}
        self.java_api_manager.compare_values(exp_res, ord_rep, "Step 2 - Check canceled order 1")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.stop_quoting_req.set_default(self.listing_id)
        self.java_api_manager.send_message(self.stop_quoting_req)
