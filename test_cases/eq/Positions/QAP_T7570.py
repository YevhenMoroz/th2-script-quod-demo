import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_cases.eq.Positions.PreConditionForPosition import PreConditionForPosition
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    OrderReplyConst, ExecutionReportConst, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7570(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.accept_request = CDOrdAckBatchRequest()
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")['OrdQty']
        self.source_acc = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.destination_acc = self.data_set.get_account_by_name('client_pos_3_acc_2')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.pos_trans = PositionTransferInstructionOMS(data_set)
        self.request_for_position = RequestForPositions()
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.qty_to_transfer = '50.0'
        self.transfer_price = '4.0'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition: Create CO order and Manual Execute its
        # part 1: Create and accept CO order
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'AccountGroupID': self.client, 'PreTradeAllocationBlock': {
                                                         'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                             {'AllocAccountID': self.source_acc,
                                                              'AllocQty': self.qty}]}}})
        self.ja_manager_second.send_message_and_receive_response(self.order_submit, response_time=25000)
        cd_ord_notif = self.ja_manager_second.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, self.desk)
        self.ja_manager.send_message_and_receive_response(self.accept_request)
        # end of part

        # part 2: Manual Execute CO order
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # end of part
        # endregion

        # region step 1-2 : Get position for needed firm accounts
        position_for_source_acc = self._extract_cum_values_for_firm_account(self.source_acc)
        common_daily_pl_before_transfer = self._extract_daily_pl_from_position_ack()
        position_for_destination_acc = self._extract_cum_values_for_firm_account(self.destination_acc)
        # endregion

        # region step 3-4: Perform Position Transfer:
        self.pos_trans.set_default_transfer(self.source_acc, self.destination_acc, self.qty_to_transfer,
                                            self.transfer_price)
        self.pos_trans.update_fields_in_component('PositionTransferInstructionBlock', {'InstrID': self.instrument_id})
        self.ja_manager.send_message_and_receive_response(self.pos_trans)
        # endregion

        # region step 5: Check PositQty and Transferred In Amt for destination account
        self._check_position_transferred_in_amt_and_posit_qty(self.destination_acc, position_for_destination_acc, True)
        # endregion

        # region step 6: Check PositQty and Transferred Out Amt for source account
        self._check_position_transferred_in_amt_and_posit_qty(self.source_acc, position_for_source_acc, False)
        # endregion

        # region step 7: Check Common Daily PL and Today Net PL
        position_response = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                [JavaApiFields.PositQty.value,
                                                                                 self.source_acc]).get_parameters() \
            [JavaApiFields.PositionReportBlock.value]
        daily_pl_actually = position_response[JavaApiFields.SecurityAccountPLBlock.value][
            JavaApiFields.TodayRealizedPL.value]
        posit_qty_source_acc_before_transfer = position_for_source_acc[JavaApiFields.PositQty.value]
        net_weighted_avg_px_before_transfer = position_for_source_acc[JavaApiFields.NetWeightedAvgPx.value]
        net_weighted_avg_px_after_transfer = PositionCalculationManager.calculate_net_weighted_avg_px_for_position_transfer_source_acc(
            posit_qty_source_acc_before_transfer,
            self.qty_to_transfer,
            net_weighted_avg_px_before_transfer,
            self.transfer_price)
        today_net_pl_before_transfer = position_for_source_acc[JavaApiFields.DailyRealizedNetPL.value]
        realized_pl = PositionCalculationManager.calculate_realized_pl_for_transfer_sell(
            posit_qty_source_acc_before_transfer, self.qty_to_transfer, self.transfer_price,
            net_weighted_avg_px_after_transfer)
        today_net_pl_after_transfer = str(float(
            today_net_pl_before_transfer) + float(realized_pl))
        expected_daily_pl = str(float(common_daily_pl_before_transfer) + float(realized_pl))
        self.ja_manager.compare_values({JavaApiFields.DailyRealizedNetPL.value: today_net_pl_after_transfer},
                                       position_response[JavaApiFields.PositionList.value][
                                           JavaApiFields.PositionBlock.value][0],
                                       f'Check that {JavaApiFields.DailyRealizedNetPL.value} has properly value (step 7)')
        self.ja_manager.compare_values({JavaApiFields.TodayRealizedPL.value: expected_daily_pl},
                                       {JavaApiFields.TodayRealizedPL.value: daily_pl_actually},
                                       f'Check that {JavaApiFields.TodayRealizedPL.value} has properly value (step 7)')
        # endregion

    def _extract_cum_values_for_firm_account(self, firm_account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              firm_account)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    def _check_position_transferred_in_amt_and_posit_qty(self, account, position_for_account, is_transfer_in):
        posit_qty_before = position_for_account[JavaApiFields.PositQty.value]
        currently_position = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                 [JavaApiFields.PositQty.value,
                                                                                  account]).get_parameters() \
            [JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        posit_qty_after = currently_position[JavaApiFields.PositQty.value]
        expected_transferred_amt = str(float(self.qty_to_transfer) * float(self.transfer_price))
        if is_transfer_in:
            expected_result = {JavaApiFields.PositQty.value: self.qty_to_transfer,
                               JavaApiFields.TransferredInAmt.value: expected_transferred_amt}
            transferred_in_amt_before = position_for_account[JavaApiFields.TransferredInAmt.value]
            transferred_in_amt_after = currently_position[JavaApiFields.TransferredInAmt.value]
            values_for_check = [{JavaApiFields.PositQty.value: str(float(posit_qty_after) - float(posit_qty_before)),
                                 JavaApiFields.TransferredInAmt.value: str(
                                     float(transferred_in_amt_after) - float(transferred_in_amt_before))},
                                'Verifying actually and expected results for step 5']
        else:
            expected_result = {JavaApiFields.PositQty.value: self.qty_to_transfer,
                               JavaApiFields.TransferredOutAmt.value: expected_transferred_amt}
            transferred_out_amt_before = position_for_account[JavaApiFields.TransferredOutAmt.value]
            transferred_out_amt_after = currently_position[JavaApiFields.TransferredOutAmt.value]
            values_for_check = [{JavaApiFields.PositQty.value: str(float(posit_qty_before) - float(posit_qty_after)),
                                 JavaApiFields.TransferredOutAmt.value: str(
                                     float(transferred_out_amt_after) - float(transferred_out_amt_before))},
                                'Verifying actually and expected results for step 6']
        self.ja_manager.compare_values(expected_result, values_for_check[0], values_for_check[1])

    def _extract_daily_pl_from_position_ack(self):
        common_daily_pl = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.SecurityAccountPLBlock.value][JavaApiFields.TodayRealizedPL.value]
        return common_daily_pl
