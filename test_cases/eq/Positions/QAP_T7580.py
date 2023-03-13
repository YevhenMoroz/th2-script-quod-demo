import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7580(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.source_acc = self.data_set.get_account_by_name("client_pos_3_acc_1")
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1,
            self.environment.get_list_fe_environment()[0].desk_ids[0],
            SubmitRequestConst.USER_ROLE_1.value)
        self.trd_entry = TradeEntryOMS(self.data_set)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        self.trd_entry.set_default_trade(ord_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trd_entry)
        exec_id = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)['ExecID']

        buy_avg_px = \
            self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, "BuyAvgPx").get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]["BuyAvgPx"]
        # endregion
        # region Step 3-5
        self.trd_entry.set_default_trade(ord_id, "15", self.qty)
        self.trd_entry.update_fields_in_component("TradeEntryRequestBlock", {"TradeEntryTransType": "REP",
                                                                             'ExecRefID': exec_id})
        self.ja_manager.send_message_and_receive_response(self.trd_entry)
        posit_block = \
            self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, "BuyAvgPx").get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({"BuyAvgPx": buy_avg_px}, posit_block, "Check BuyAvgPx",
                                       VerificationMethod.NOT_EQUALS)
        # endregion
