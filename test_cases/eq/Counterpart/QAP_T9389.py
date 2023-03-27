import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, OrderReplyConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9389(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_conn_2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_conn_2, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.manual_execute = TradeEntryOMS(self.data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.complete_reqeust = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order:
        recipient = self.environment.get_list_fe_environment()[0].user_1
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        role = SubmitRequestConst.USER_ROLE_1.value
        self.order_submit.set_default_care_limit(recipient=recipient,
                                                 desk=desk,
                                                 role=role)
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        qty = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, f'Verify that order {order_id} has Sts = Open')
        # endregion

        # region step 2 : Manually execute CO order via JavaApiUser_2
        half_qty = str(float(qty) / 2)
        self.manual_execute.set_default_trade(order_id, price, half_qty)
        self.java_api_manager2.send_message_and_receive_response(self.manual_execute)
        execution_report = \
            self.java_api_manager2.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, f'Verifying that {order_id} has ExecSts = '
                              f'{ExecutionReportConst.TransExecStatus_PFL.value}, (step 2)')

        # endregion

        # region step 3: Create Child CO order
        self.order_submit.set_default_child_care(recipient, desk, role, order_id)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.OrdQty.value: half_qty
        })
        self.java_api_manager2.send_message_and_receive_response(self.order_submit)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager2.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        child_ord_id = order_notif_message[JavaApiFields.OrdID.value]
        self.java_api_manager2.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                              order_notif_message, f'Verify that  Child Order {child_ord_id} '
                                                                   f'has Sts = Sent (step 3)')
        # endregion

        # region step 4:Accept Child CO order
        self.accept_request.set_default(child_ord_id, cd_order_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, f'Check that {child_ord_id} has Sts = Open (step 4)')
        # endregion

        # region step 5: Fully Filled Child CO order
        self.manual_execute.set_default_trade(child_ord_id, price, half_qty)
        self.java_api_manager.send_message_and_receive_response(self.manual_execute,
                                                                {order_id: order_id, child_ord_id: child_ord_id})
        execution_report_child_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                              child_ord_id).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report_child_order,
            f'Verifying that Child order {order_id} is {ExecutionReportConst.TransExecStatus_FIL.value} (step 5)')
        execution_report_parent_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                               order_id).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report_parent_order, f'Verifying that {order_id} has ExecSts = '
                                           f'{ExecutionReportConst.TransExecStatus_FIL.value}, (step 5)')
        # endergion

        # region step 6: Complete CO order
        self.complete_reqeust.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_reqeust)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply_message,
            'Verifying expected and actually results (step 6)')
        # endregion

        # region step 7: Book Parent CO order
        self.allocation_instruction.set_default_book(order_id)
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}, ord_update,
            'Verifying that order booked (step 7)')
        # endregion

        # region step 8: Check 35 = J message
        last_user_conterpart = self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2')
        route_counterpart = self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route')
        regulatory_body = self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris')
        entering_firm = self.data_set.get_counterpart_id_fix('entering_firm')
        change_parameters = {
            'AllocType': 5,
            'NoParty': [route_counterpart,
                        last_user_conterpart,
                        regulatory_body,
                        entering_firm],
            'NoOrders': [{
                'ClOrdID': cl_ord_id,
                'OrderID': order_id
            }],
        }

        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime', 'AllocInstructionMiscBlock1',
                                  'AllocTransType', 'ReportedPx', 'Side',
                                  'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'NoPartySubIDs',
                                  'AllocID', 'Currency', 'NetMoney', 'Instrument',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocQty', 'AllocPrice', 'OrderAvgPx']
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        # endregion
