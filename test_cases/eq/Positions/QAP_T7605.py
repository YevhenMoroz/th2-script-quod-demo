import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    OrderReplyConst, ExecutionReportConst, SubscriptionRequestTypes, PosReqTypes
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
class QAP_T7605(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.client_2 = self.data_set.get_client_by_name('client_1')
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)

        self.accept_request = CDOrdAckBatchRequest()
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.instrument_id = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[
            JavaApiFields.InstrID.value]
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.dma_wash_book = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.request_for_position = RequestForPositions()
        self.rule_manager = RuleManager(Simulators.equity)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.booking_cancel_request = BookingCancelRequest()
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-2-3: Create CO orders:
        first_qty = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                                  JavaApiFields.OrdQty.value]
        second_qty = '400'
        result_for_wb1_new = self._extract_cum_values_for_washbook(self.wash_book)
        cum_sell_qty_initial = result_for_wb1_new[JavaApiFields.CumSellQty.value]
        posit_qty_initial = result_for_wb1_new[JavaApiFields.PositQty.value]
        tuple_ord_id_and_clordid = self._create_co_orders('step 1', first_qty, self.client)
        order_id = tuple_ord_id_and_clordid[0]
        cl_ord_id = tuple_ord_id_and_clordid[1]
        tuple_ord_id_and_clordid_second = self._create_co_orders('step 2', second_qty, self.client_2)
        order_id_second = tuple_ord_id_and_clordid_second[0]
        cl_ord_id_second = tuple_ord_id_and_clordid_second[1]
        # endregion

        # region step  4-7: Create Child DMA order and trade it
        route_params = {JavaApiFields.RouteBlock.value: [
            {JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self._trade_child_dma_order(first_qty, order_id, self.client, cl_ord_id, 'step 4', route_params)
        position_report_first = self.ja_manager.get_last_message(PKSMessageType.PositionReport.value, [self.wash_book,
                                                                                                       JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        first_qty = str(float(first_qty))
        self.ja_manager.compare_values({
            JavaApiFields.CumSellQty.value: first_qty,
            JavaApiFields.PositQty.value: first_qty}, {
            JavaApiFields.CumSellQty.value: str(
                float(position_report_first[JavaApiFields.CumSellQty.value]) - float(cum_sell_qty_initial)),
            JavaApiFields.PositQty.value: float(posit_qty_initial) - float(
                position_report_first[JavaApiFields.PositQty.value])},
            f'Verify that {JavaApiFields.CumSellQty.value} increased and {JavaApiFields.PositQty.value} decreased on {first_qty} (step 5)')

        self._trade_child_dma_order(second_qty, order_id_second, self.client_2, cl_ord_id_second, 'step 6', route_params)
        position_report_second = self.ja_manager.get_last_message(PKSMessageType.PositionReport.value, [self.wash_book,
                                                                                                        JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        second_qty = str(float(second_qty))
        self.ja_manager.compare_values({
            JavaApiFields.CumSellQty.value: second_qty,
            JavaApiFields.PositQty.value: second_qty
        },
            {
                JavaApiFields.CumSellQty.value: str(
                    float(position_report_second[JavaApiFields.CumSellQty.value]) - float(
                        position_report_first[JavaApiFields.CumSellQty.value])),
                JavaApiFields.PositQty.value: str(
                    float(position_report_first[JavaApiFields.PositQty.value]) - float(
                        position_report_second[JavaApiFields.PositQty.value]))
            },
            f'Verify that {JavaApiFields.CumSellQty.value} increased and {JavaApiFields.PositQty.value} decreased on {second_qty} (step 7)')

        # region step 8 complete and book Care Orders
        self._complete_and_book_co_order(first_qty, order_id, self.client, 'step 8')
        # region step 9:Check Position
        position_report_first_block = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [JavaApiFields.PositQty.value,
                                                                 self.wash_book]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({JavaApiFields.PositQty.value: first_qty,
                                        JavaApiFields.CumSellQty.value: first_qty},
                                       {JavaApiFields.PositQty.value: str(
                                           float(position_report_first_block[JavaApiFields.PositQty.value]) - float(
                                               position_report_second[JavaApiFields.PositQty.value])),
                                           JavaApiFields.CumSellQty.value: str(
                                               float(position_report_second[JavaApiFields.CumSellQty.value]) - float(
                                                   position_report_first_block[JavaApiFields.CumSellQty.value]))},
                                       f'Verify that {JavaApiFields.CumSellQty.value} decreased and {JavaApiFields.PositQty.value} increased on {first_qty} (step 9)')
        # endregion

        # region step 10 complete and book Care Orders
        self._complete_and_book_co_order(second_qty, order_id_second, self.client_2, 'step 10')
        # endregion

        # region step 11:Check Position
        position_report_second_block = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [JavaApiFields.PositQty.value,
                                                                 self.wash_book]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({JavaApiFields.PositQty.value: first_qty,
                                        JavaApiFields.CumSellQty.value: first_qty},
                                       {JavaApiFields.PositQty.value: str(
                                           float(position_report_second_block[JavaApiFields.PositQty.value]) - float(
                                               position_report_first_block[JavaApiFields.PositQty.value])),
                                           JavaApiFields.CumSellQty.value: str(
                                               float(
                                                   position_report_first_block[JavaApiFields.CumSellQty.value]) - float(
                                                   position_report_second_block[JavaApiFields.CumSellQty.value]))},
                                       f'Verify that {JavaApiFields.CumSellQty.value} decreased and {JavaApiFields.PositQty.value} increased on {first_qty} (step 11)')
        # endregion

    def _create_co_orders(self, step, qty, client):
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.AccountGroupID.value: client,
            JavaApiFields.WashBookAccountID.value: self.wash_book,
            JavaApiFields.OrdQty.value: qty,
            JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
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
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply,
                                       f'Verifying that order has properly status ({step})')
        return order_id, cl_ord_id

    def _trade_child_dma_order(self, qty, order_id, client, cl_ord_id, step, route_params):
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client, self.mic, float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client, self.mic,
                                                                                            float(self.price),
                                                                                            int(qty), 0)
            self.order_submit.get_parameters().clear()
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {
                                                             JavaApiFields.OrdQty.value: qty,
                                                             JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
                                                             JavaApiFields.AccountGroupID.value: client,
                                                             JavaApiFields.RouteList.value: route_params,
                                                             JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                                                             JavaApiFields.WashBookAccountID.value: self.dma_wash_book
                                                         })
            self.ja_manager.send_message_and_receive_response(self.order_submit, {cl_ord_id: cl_ord_id})
            execution_report = self.ja_manager_second.get_last_message_by_multiple_filter(
                ORSMessageType.ExecutionReport.value, [order_id]).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.ja_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report,
                f'Verify that order filled {step}')
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)

    def _complete_and_book_co_order(self, qty, order_id, client, step):
        self.ja_manager.send_message_and_receive_response(self.complete_request.set_default_complete(order_id))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.Qty.value: qty,
                                                                   JavaApiFields.AccountGroupID.value: client
                                                               })
        self.ja_manager.send_message_and_receive_response(self.allocation_instruction)
        order_update = self.ja_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.ja_manager.compare_values({JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
                                       order_update, f'Verify that {order_id} order booked ({step})')

    def _extract_cum_values_for_washbook(self, washbook):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              washbook)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][
            JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
