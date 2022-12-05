import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7376(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send Fees
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(
            fee_type=self.data_set.get_misc_fee_type_by_name("agent"), comm_profile=self.perc_amt
        )
        self.rest_commission_sender.change_message_params(
            {
                "venueID": self.data_set.get_venue_by_name("venue_2"),
                "contraFirmCounterpartID": self.data_set.get_counterpart_id("contra_firm"),
            }
        )
        self.rest_commission_sender.send_post_request()
        time.sleep(3)
        # endregion

        # region Step 1 - Create CO
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "AccountGroupID": self.client,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value
        )["OrdID"]

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Comparing Status of Care order",
        )
        # endregion

        # region Step 2 - Execute CO
        self.trade_request.set_default_trade(order_id)
        self.trade_request.update_fields_in_component(
            "TradeEntryRequestBlock",
            {
                "CounterpartList": {
                    "CounterpartBlock": [self.data_set.get_counterpart_id_java_api("counterpart_contra_firm")]
                }
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        expected_result = {"TransExecStatus": "FIL", "ExecCommission": "0.5"}
        self.java_api_manager.compare_values(expected_result, exec_reply, "Compare TransExecStatus and ExecCommission")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
