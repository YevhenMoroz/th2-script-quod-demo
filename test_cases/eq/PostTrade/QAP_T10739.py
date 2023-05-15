import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiSettlementModelMessages import RestApiSettlementModelMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10739(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1,
            self.environment.get_list_fe_environment()[0].desk_ids[0], SubmitRequestConst.USER_ROLE_1.value)
        self.rest_api_conn = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.rest_api_conn, self.test_id)
        self.api_message = RestApiSettlementModelMessages(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.book_request = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        vanue_id = self.data_set.get_venue_id('paris')
        self.api_message.set_modify_message_clear()
        self.api_message.update_parameters({"venueID": vanue_id, "instrumentGroupID": 1})
        self.rest_api_manager.send_post_request(self.api_message)
        # endregion
        # region Step 1
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region Step 2
        self.trade_entry.set_default_trade(ord_id)
        self.ja_manager.send_message(self.trade_entry)
        # endregion
        # region Step 3
        self.complete_message.set_default_complete(ord_id)
        self.ja_manager.send_message(self.complete_message)
        self.book_request.set_default_book(ord_id)
        self.ja_manager.send_message_and_receive_response(self.book_request)
        allocation_report = \
            self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.ja_manager.compare_values({"SettlementModelID": "3"}, allocation_report, "Check Settlement")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.api_message.set_modify_message_clear()
        self.rest_api_manager.send_post_request(self.api_message)
