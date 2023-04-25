import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    OrderReplyConst, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7198(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)

        self.accept_request = CDOrdAckBatchRequest()
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.qty = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.OrdQty.value]
        self.instrument_id = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[
            JavaApiFields.InstrID.value]
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.request_for_position = RequestForPositions()
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.booking_cancel_request = BookingCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step precondition: Create CO order:
        result_for_wb1_new = self._extract_cum_values_for_washbook(self.wash_book)
        cum_by_qty_initial = result_for_wb1_new[JavaApiFields.CumBuyQty.value]
        posit_qty_initial = result_for_wb1_new[JavaApiFields.PositQty.value]
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.WashBookAccountID.value: self.wash_book,
            JavaApiFields.ClOrdID.value: bca.client_orderid(9)})
        self.ja_manager_second.send_message_and_receive_response(self.order_submit)
        cd_ord_notif = self.ja_manager_second.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, self.desk)
        self.ja_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply,
                                       'Verifying that order has properly status')
        # endregion

        # region manual execute CO order (step 2)
        self.qty = str(float(self.qty))
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.PositQty.value,
                                                                               self.wash_book]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({
            'IncreasedPositQty': self.qty,
            'IncreasedCumBuyQty': self.qty
        }, {'IncreasedPositQty': str(float(position_report[JavaApiFields.PositQty.value]) - float(posit_qty_initial)),
            'IncreasedCumBuyQty': str(
                float(position_report[JavaApiFields.CumBuyQty.value]) - float(cum_by_qty_initial))},
            f'Verify that {JavaApiFields.CumBuyQty.value} and {JavaApiFields.PositQty.value} increased on {self.qty} (step 1)')
        # endregion

        # region step 2: Complete CO order
        self.ja_manager.send_message_and_receive_response(
            self.complete_request.set_default_complete(order_id))
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply,
            "Verifying values (step 2)")
        # endregion

        # region step 3: Book order
        self.allocation_instruction.set_default_book(order_id)
        self.ja_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                             JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.BookingAllocInstructionID.value]
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.PositQty.value,
                                                                               self.wash_book]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({
            JavaApiFields.PositQty.value: posit_qty_initial,
            JavaApiFields.CumBuyQty.value: cum_by_qty_initial
        }, position_report,
            f'Verify that {JavaApiFields.CumBuyQty.value} and {JavaApiFields.PositQty.value} decreased on {self.qty} (step 3)')
        # endregion

        # region step 4: unbook order
        self.booking_cancel_request.set_default(alloc_id)
        self.ja_manager.send_message_and_receive_response(self.booking_cancel_request)
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.PositQty.value,
                                                                               self.wash_book]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({
            'IncreasedPositQty': self.qty,
            'IncreasedCumBuyQty': self.qty
        }, {'IncreasedPositQty': str(float(position_report[JavaApiFields.PositQty.value]) - float(posit_qty_initial)),
            'IncreasedCumBuyQty': str(
                float(position_report[JavaApiFields.CumBuyQty.value]) - float(cum_by_qty_initial))},
            f'Verify that {JavaApiFields.CumBuyQty.value} and {JavaApiFields.PositQty.value} increased on {self.qty} (step 4)')

        # endregion

    def _extract_cum_values_for_washbook(self, washbook):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              washbook)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
