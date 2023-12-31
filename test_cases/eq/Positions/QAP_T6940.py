import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes, \
    OrderReplyConst, ExecutionReportConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6940(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = '2'
        self.qty = '120'
        self.request_for_position = RequestForPositions()
        self.sec_account = self.data_set.get_account_by_name("client_pos_3_acc_4")  # "PROP_TEST"
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.cancel_request = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precodition: Set up Fees
        self.rest_commission_sender.clear_fees()
        perc_amt = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('paris')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=perc_amt, fee=fee)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
            'instrType': instr_type,
        })
        self.rest_commission_sender.send_post_request()
        # endregion

        # region step 1: Create DMA order
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.PreTradeAllocationBlock.value: {
                                                         JavaApiFields.PreTradeAllocationList.value: {
                                                             JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                 {JavaApiFields.AllocAccountID.value: self.sec_account,
                                                                  JavaApiFields.AllocQty.value: self.qty}]}},
                                                         JavaApiFields.AccountGroupID.value: self.client,
                                                         JavaApiFields.OrdQty.value: self.qty,
                                                         JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
                                                         JavaApiFields.Price.value: self.price})
        self.ja_manager.send_message_and_receive_response(self.order_submit, response_time=15_000)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                       order_reply, 'Verify that order created (step 1)')
        order_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region step 2: Partially Fill DMA order
        position = self._extract_cum_values_for_acc(self.sec_account)
        self.exec_rep.set_default_trade(order_id)
        trade_qty = '50'
        remaining_qty = str(float(self.qty) - float(trade_qty))
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                 {
                                                     JavaApiFields.OrdQty.value: self.qty,
                                                     JavaApiFields.LastTradedQty.value: trade_qty,
                                                     JavaApiFields.LastPx.value: self.price,
                                                     JavaApiFields.Price.value: self.price,
                                                     JavaApiFields.Side.value:SubmitRequestConst.Side_Sell.value,
                                                     JavaApiFields.LeavesQty.value: remaining_qty,
                                                     JavaApiFields.CumQty.value: trade_qty,
                                                     JavaApiFields.AvgPrice.value: self.price
                                                 })
        self.ja_manager.send_message_and_receive_response(self.exec_rep)
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verify that DMA order partially filled (step 2)')
        # endregion

        # region step 3: Check that SellAvgPx has properly calculated value
        sell_avg_px_before = position[JavaApiFields.SellAvgPx.value]
        posit_qty_before = position[JavaApiFields.PositQty.value]
        position_after_first_trade = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [JavaApiFields.PositQty.value,
                                                                 self.sec_account]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        fees = float(trade_qty) * float(self.price) / 100 * float(5)
        sell_avg_px_expected = PositionCalculationManager.calculate_sell_avg_px_execution_sell_side_net(posit_qty_before,
                                                                                                 trade_qty, self.price,
                                                                                                 sell_avg_px_before,
                                                                                                 fees=str(fees))
        self.ja_manager.compare_values({JavaApiFields.SellAvgPx.value: sell_avg_px_expected},
                                       position_after_first_trade,
                                       f'Verify that {JavaApiFields.SellAvgPx.value} of {self.sec_account} has properly calculated value (step 3)')
        # endregion

        # region step 4: Trade DMA order again
        remaining_qty = float(remaining_qty) - float(trade_qty)
        second_price = '1.2'
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                 {
                                                     JavaApiFields.OrdQty.value: self.qty,
                                                     JavaApiFields.LastTradedQty.value: trade_qty,
                                                     JavaApiFields.LastPx.value: second_price,
                                                     JavaApiFields.Price.value: second_price,
                                                     JavaApiFields.LeavesQty.value: remaining_qty,
                                                     JavaApiFields.CumQty.value: trade_qty,
                                                     JavaApiFields.VenueExecID.value: bca.client_orderid(9),
                                                     JavaApiFields.AvgPrice.value: '1.6'
                                                 })
        self.ja_manager.send_message_and_receive_response(self.exec_rep)
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verify that DMA order partially filled (step 4)')
        # endregion

        # region step 5 : Verify that SellAvgPx value calculated properly
        position_after_second_trade = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [JavaApiFields.PositQty.value,
                                                                 self.sec_account]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        fees = float(trade_qty) * float(second_price) / 100 * float(5)
        posit_qty_before_second_trade = position_after_first_trade[JavaApiFields.PositQty.value]
        sell_avg_px_expected_after_second_trade = PositionCalculationManager.calculate_sell_avg_px_execution_sell_side_net(
            posit_qty_before_second_trade,
            trade_qty, second_price,
            sell_avg_px_expected,
            fees=str(fees))
        self.ja_manager.compare_values({JavaApiFields.SellAvgPx.value: sell_avg_px_expected_after_second_trade},
                                       position_after_second_trade,
                                       f'Verify that {JavaApiFields.SellAvgPx.value} of {self.sec_account} has properly calculated value (step 5)')
        # endregion

        # region step 6: Cancel DMA order
        order_cancel_rule = None
        try:
            order_cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, True)
            self.cancel_request.set_default(order_id)
            self.ja_manager.send_message_and_receive_response(self.cancel_request)
            ord_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                        OrderReplyConst.TransStatus_CXL.value).get_parameter(
                JavaApiFields.OrdReplyBlock.value)
            self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value},
                                                 ord_reply, 'Verify that order canceled (step 6)')
            position_after_cancel = \
                self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                    [JavaApiFields.PositQty.value,
                                                                     self.sec_account]).get_parameters()[
                    JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                    JavaApiFields.PositionBlock.value][0]
            self.ja_manager.compare_values({JavaApiFields.SellAvgPx.value: sell_avg_px_expected_after_second_trade},
                                           position_after_cancel,
                                           f'Verify that {JavaApiFields.SellAvgPx.value} does not change (step 6)')
        except Exception as ex:
            logger.exception(f'{ex} - your exception', exc_info=True)
        finally:
            self.rule_manager.remove_rule(order_cancel_rule)
        # endregion

    def _extract_cum_values_for_acc(self, acc):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              acc)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
