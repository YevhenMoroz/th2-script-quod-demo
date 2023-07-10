import logging
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
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
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.qs_messages.ListingQuotingModificationRequest import (
    ListingQuotingModificationRequest,
)
from test_framework.java_api_wrappers.qs_messages.QuoteManagementRequest import QuoteManagementRequest
from test_framework.java_api_wrappers.qs_messages.StopQuotingRequest import StopQuotingRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10165(TestCase):
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
        self.listing_id = self.data_set.get_listing_id_by_name("listing_3")
        self.instrument = self.data_set.get_java_api_instrument("instrument_2")
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_qs.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_qs.xml"
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.quote_status_report = QuoteStatusReport(self.data_set)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
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

        # region Setup QS config
        tree = ET.parse(self.local_path)
        partial_fill_stop = tree.getroot().find("qs/partialFillStop")
        partial_fill_stop.text = "true"
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QS")
        time.sleep(90)

        # region Setup Market Data
        md_req_id = self.market_data_refresh.get_MDReqID(self.listing_id, self.fix_env.feed_handler)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "1", best_ask, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "0", best_bid, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        self.market_data_refresh.set_market_data_incr_refresh(md_req_id, "1", "2", last_trd_px, size)
        self.fix_manager_fh.send_message(self.market_data_refresh)
        # endregion

        # region Step 1-3: Start quoting
        self.listing_quote.set_default(self.listing_id, spread_px_type="PRC", bid_spread=spread, offer_spead=spread)
        self.java_api_manager.send_message(self.listing_quote)

        bid_px: str = str(float(last_trd_px) - float(spread))
        offer_px: str = str(float(last_trd_px) + float(spread))
        self.quote_request.set_default(self.listing_id, offer_px, bid_px, offer_size, bid_size)
        self.java_api_manager.send_message_and_receive_response(self.quote_request)

        quote_rep = self.java_api_manager.get_last_message(QSMessageType.QuoteStatusReport.value).get_parameters()[
            "QuoteStatusReportBlock"]
        quote_id = quote_rep["QuoteID"]
        self.java_api_manager.compare_values({"QuoteStatus": "ACK", "BidPx": bid_px, "OfferPx": offer_px}, quote_rep,
                                             "Check quote")
        # endregion
        # region Step 4-5: Execute quote
        new_ord_id = basic_custom_actions.client_orderid(9)
        self.exec_rep.set_default_trade(new_ord_id)
        self.exec_rep.update_fields_in_component("ExecutionReportBlock", {"InstrumentBlock": self.instrument
            , "QuoteMsgID": quote_id, "LastPx": bid_px, "AvgPrice": bid_px})
        self.java_api_manager.send_message(self.exec_rep)
        self.quote_status_report.set_default(quote_id, "CXL")
        self.java_api_manager.send_message(self.quote_status_report)
        time.sleep(3)
        res = self.db_manager.execute_query(f"SELECT quotestatus FROM quote WHERE quoteid = '{quote_id}'")
        self.java_api_manager.compare_values({"quotestatus": "CXL"}, {"quotestatus": res[0][0]}, "Check quote status")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QS")
        time.sleep(90)
        os.remove("temp.xml")
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
