import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import QSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageMarketDataIncrementalRefreshOMS import (
    FixMessageMarketDataIncrementalRefreshOMS,
)
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.es_messages.QuoteStatusReport import QuoteStatusReport
from test_framework.java_api_wrappers.qs_messages.ListingQuotingModificationRequest import (
    ListingQuotingModificationRequest,
)
from test_framework.java_api_wrappers.qs_messages.QuoteManagementRequest import QuoteManagementRequest
from test_framework.java_api_wrappers.qs_messages.StopQuotingRequest import StopQuotingRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10186(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.listing_quote = ListingQuotingModificationRequest()
        self.quote_request = QuoteManagementRequest()
        self.market_data_refresh = FixMessageMarketDataIncrementalRefreshOMS()
        self.stop_quoting_req = StopQuotingRequest()
        self.listing_id = self.data_set.get_listing_id_by_name("listing_1")
        self.quote_status_report = QuoteStatusReport(self.data_set)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.instrument = self.data_set.get_instrument_id_by_name("instrument_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
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

        # region Setup Market Data
        md_req_id = self.market_data_refresh.get_MDReqID(self.listing_id, self.fix_env.feed_handler)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "1", best_ask, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "0", best_bid, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "2", last_trd_px, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        # endregion
        # region Step 1-2: Start quoting
        self.listing_quote.set_default(self.listing_id, spread_px_type="PRC", bid_spread=spread, offer_spead=spread)
        self.java_api_manager.send_message(self.listing_quote)

        bid_px: str = str(float(last_trd_px) - float(spread))
        offer_px: str = str(float(last_trd_px) + float(spread))
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, offer_size, bid_size)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(offer_px))
            nos_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(bid_px))
            self.java_api_manager.send_message_and_receive_response(self.quote_request)
        except Exception as e:
            logger.error(f'Your Exception is {e}')
            # endregion
        finally:
            time.sleep(3)
            self.rule_manager.remove_rules([nos_rule, nos_rule2])

        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters()[
            "QuoteStatusReportBlock"]
        quote_id = quote_rep["QuoteID"]
        self.java_api_manager.compare_values({"QuoteStatus": "ACK"}, quote_rep,
                                             "Check quote")
        # endregion
        # region Step 3: Check position
        query = f"SELECT  leavesbuyqty, leavessellqty FROM posit WHERE accountid = '{self.washbook}' " \
                f"and instrid = '{self.instrument}' and positiontype = 'N'"
        res = self.db_manager.execute_query(query)
        buy_qty = res[0][0]
        sell_qty = res[0][1]
        # endregion
        # region Step 4-5: Modify quote
        bid_size = "500"
        offer_size = "500"
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, offer_size, bid_size)
        self.java_api_manager.send_message(self.quote_request)
        self.quote_status_report.set_default(quote_id, "CXL")
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(offer_px))
            nos_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, float(bid_px))
            cr_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.exec_destination, True)
            self.java_api_manager.send_message(self.quote_status_report)
        except Exception as e:
            logger.error(f'Your Exception is {e}')
            # endregion
        finally:
            time.sleep(3)
            self.rule_manager.remove_rules([cr_rule, nos_rule, nos_rule2])
        res = self.db_manager.execute_query(f"SELECT quotestatus FROM quote WHERE quoteid = '{quote_id}'")
        self.java_api_manager.compare_values({"quotestatus": "CXL"}, {"quotestatus": res[0][0]}, "Check quote status")
        # endregion
        # region Step 6: Check position
        res = self.db_manager.execute_query(query)
        buy_qty_new = float(res[0][0])
        sell_qty_new = float(res[0][1])
        buy_qty_exp = float(buy_qty) - float(bid_size)
        sell_qty_exp = float(sell_qty) - float(offer_size)
        print(f"buy_qty_new = {buy_qty_new}, buy_qty_exp = {buy_qty_exp}, buy_qty = {buy_qty}")
        self.java_api_manager.compare_values({"LeavesBuyQty": buy_qty_exp, "LeavesSellQty": sell_qty_exp}, {
            "LeavesBuyQty": buy_qty_new, "LeavesSellQty": sell_qty_new}, "Check Positions")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.stop_quoting_req.set_default(self.listing_id)
        self.java_api_manager.send_message(self.stop_quoting_req)
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
