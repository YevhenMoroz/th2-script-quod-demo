import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8860(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.request_for_position = RequestForPositions()
        self.position_transfer = PositionTransferInstructionOMS(self.data_set)
        self.qty = '500'
        self.price = '10'
        self.transfer_qty = '100.0'
        self.care_washbook = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.dma_washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition: Create CO order and execute its:
        # part 1: Create CO order:
        order_id = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.WashBookAccountID.value: self.care_washbook,
            'Side': SubmitRequestConst.Side_Buy.value,
            "ClOrdID": bca.client_orderid(9)})
        # end_of_part

        # part 2: Trade CO order
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # end_of_part

        # region step 1-2: Extract position before transfer
        position_of_care_wb_before_transfer = self._extract_cum_values_for_account(self.care_washbook)
        position_of_dma_wb_before_transfer = self._extract_cum_values_for_account(self.dma_washbook)
        # endregion

        # region step 4-5: Transfer and verifying results
        self.position_transfer.set_default_transfer(self.care_washbook, self.dma_washbook, self.transfer_qty)
        self.position_transfer.update_fields_in_component('PositionTransferInstructionBlock', {
            'InstrID': self.instrument_id,
        })
        self.ja_manager.send_message_and_receive_response(self.position_transfer)
        position_of_care_wb_after_transfer = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [self.care_washbook,
                                                                 JavaApiFields.PositQty.value]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        position_of_dma_wb_after_transfer = \
            self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                [self.dma_washbook,
                                                                 JavaApiFields.PositQty.value]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        actually_increased_qty_for_dma_wb = str(
            float(position_of_dma_wb_after_transfer[JavaApiFields.PositQty.value]) - \
            float(position_of_dma_wb_before_transfer[JavaApiFields.PositQty.value]))

        self.ja_manager.compare_values({"ExpectedDecreasedQty": self.transfer_qty},
                                       {"ExpectedDecreasedQty": actually_increased_qty_for_dma_wb},
                                       f'check that {self.dma_washbook} positon increased on {self.transfer_qty} (step 4)'
                                       )
        actually_decreasing_qty_for_dma_wb = str(
            float(position_of_care_wb_before_transfer[JavaApiFields.PositQty.value]) - \
            float(position_of_care_wb_after_transfer[JavaApiFields.PositQty.value]))
        self.ja_manager.compare_values({"ExpectedDecreasedQty": self.transfer_qty},
                                       {"ExpectedDecreasedQty": actually_decreasing_qty_for_dma_wb},
                                       f'check that {self.care_washbook} positon decreased on {self.transfer_qty} (step 5)'
                                       )

        # endregion

    def _create_orders(self, dictionary_with_needed_tags):
        self.order_submit = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", dictionary_with_needed_tags)
        self.ja_manager_second.send_message_and_receive_response(self.order_submit)
        cd_ord_notif = self.ja_manager_second.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, self.desk)
        self.ja_manager.send_message_and_receive_response(self.accept_request)
        return order_id

    def _extract_cum_values_for_account(self, account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              account)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
