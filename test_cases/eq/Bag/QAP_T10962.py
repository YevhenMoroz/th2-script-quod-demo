import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, BagChildCreationPolicy, OrderBagConst, PositionValidities
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10962(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.ord_sub = OrderSubmitOMS(self.data_set)
        self.ord_sub2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.recipient = self.environment.get_list_fe_environment()[0].user_1
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.bag_creation_request = OrderBagCreationRequest()
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.modification_request = OrderModificationRequest()
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_3')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        qty = "3000"
        slice_price = "11.0"
        # endregion

        # region Step 1: Create Care Order
        self.ord_sub.set_default_care_limit(recipient=self.recipient, desk=self.desk)
        self.ord_sub.update_fields_in_component("NewOrderSingleBlock", {'OrdQty': qty})
        self.price = self.ord_sub.get_parameter("NewOrderSingleBlock")["Price"]
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        ord_id_care = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 1: Checking Status of created Care order",
        )
        # endregion

        # region Step 2-3: Create 3 Child Care Orders
        # subregion Step 2-3: Create 1st Child Order
        child_qty1 = "500"
        self.ord_sub.set_default_child_care(recipient=self.recipient, desk=self.desk, parent_id=ord_id_care)
        self.ord_sub.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": child_qty1})
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2-3: Checking Status of 1st Child Care order",
        )
        child_ord_id_care1 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]

        # subregion Step 2-3: Create 2nd Child Order
        child_qty2 = "1000"
        self.ord_sub.set_default_child_care(recipient=self.recipient, desk=self.desk, parent_id=ord_id_care)
        self.ord_sub.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": child_qty2})
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2-3: Checking Status of 2nd Child Care order",
        )
        child_ord_id_care2 = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]

        # subregion Step 2-3: Create 3rd Child Order
        child_qty3 = "1500"
        self.ord_sub.set_default_child_care(recipient=self.recipient, desk=self.desk, parent_id=ord_id_care)
        self.ord_sub.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": child_qty3})
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2-3: Checking Status of 3rd Child Care order",
        )
        child_ord_id_care3 = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        child_orders_id = [child_ord_id_care1, child_ord_id_care2, child_ord_id_care3]
        # endregion

        # region Step 4: Create Bag
        bag_name = 'QAP_T10962'
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, child_orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        self.java_api_manager.compare_values(expected_result, order_bag_notification, "Step 4: Check created Bag")
        # endregion

        # region Step 5: Create Slice Order grom Bag
        client_ord_id = bca.client_orderid(9)
        slice_order_id = None
        self.ord_sub2.set_default_care_limit(recipient=self.recipient, desk=self.desk)
        self.ord_sub2.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         'AvgPriceType': "EA",
                                                         'ExternalCare': 'N',
                                                         'SlicedOrderBagID': bag_order_id,
                                                         'OrdQty': qty,
                                                         'Price': slice_price,
                                                         'ClOrdID': client_ord_id
                                                     })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(slice_price))
            self.java_api_manager.send_message_and_receive_response(self.ord_sub2)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Step 5: Checking that Slice order created')
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)

        # region Step 6: Manual execute sliced order
        # subregion Step 6: Send manual execution request
        exec_qty = "2000"
        self.trade_entry_request.set_default_trade(slice_order_id, slice_price, exec_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)

        # subregion Step 6: Check execution for sliced order
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id = exec_report_block['ExecID']
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, exec_report_block,
            'Step 6-7: Check execution of sliced order')
        self._verify_order(child_orders_id, 'PFL', ["167.0", "334.0", "499.0"], '6-7')
        # endregion

        # region Step 8: trade cancel
        # subregion Step 8: Send cancel execution request
        self.trade_entry_request.set_default_cancel_execution(slice_order_id, exec_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)

        # subregion Step 8: check cancelled exec
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
            exec_report_block,
            'Step 8 - Check execution of order after trade cancellation')

        # subregion Step 8: Verify unmatchedQty for child orders
        self._verify_order(child_orders_id, None, [str(child_qty1)+'.0', str(child_qty2)+'.0', str(child_qty3)+'.0'], '8')
        # endregion

    def _verify_order(self, orders_id, order_status, unmatched_qty_list, step):
        for n, ord_id in enumerate(orders_id):
            self.modification_request.set_default(self.data_set, ord_id)
            self.modification_request.remove_fields_from_component("OrderModificationRequestBlock", ['Price', 'OrdQty'])
            self.modification_request.update_fields_in_component(
                "OrderModificationRequestBlock", {JavaApiFields.PosValidity.value: PositionValidities.PosValidity_DEL.value,
                                                  JavaApiFields.WashBookAccountID.value: self.washbook}
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            expected_result = {JavaApiFields.UnmatchedQty.value: unmatched_qty_list[n]}
            if order_status:
                expected_result[JavaApiFields.TransExecStatus.value] = order_status
            self.java_api_manager.compare_values(
                expected_result,
                order_reply,
                f"Step {step}: Comparing fields for {ord_id} order",
            )

