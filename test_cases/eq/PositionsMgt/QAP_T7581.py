import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7581(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_first = self.data_set.get_client_by_name("client_pos_3")
        self.client_second = self.data_set.get_client_by_name('client_pos_1')
        self.source_acc = self.data_set.get_account_by_name("client_pos_3_acc_4")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.request_for_position = RequestForPositions()
        self.qty_of_first_order = '200'
        self.price_of_first_order = '10'
        self.qty_of_second_order = '100'
        self.price_of_second_order = '10'
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition: Create CO orders and execute its:
        # part 1: Create CO orders:
        order_id_first = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty_of_first_order,
            JavaApiFields.Price.value: self.price_of_first_order,
            "PreTradeAllocationBlock": {
                "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                    {"AllocAccountID": self.source_acc, "AllocQty": self.qty_of_first_order}]}},
            'Side': SubmitRequestConst.Side_Buy.value,
            "AccountGroupID": self.client_first,
            "ClOrdID": bca.client_orderid(9)})
        order_id_second = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty_of_second_order,
            JavaApiFields.Price.value: self.price_of_second_order,
            JavaApiFields.WashBookAccountID.value: self.wash_book,
            'Side': SubmitRequestConst.Side_Buy.value,
            "AccountGroupID": self.client_second,
            "ClOrdID": bca.client_orderid(9)})
        # end_of_part

        # part 2: Trade CO orders
        # sub_part 1:Trade First CO order via Manual Execution
        self.trade_entry.set_default_trade(order_id_first, self.price_of_first_order, self.qty_of_first_order)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # end_of_sub_part
        # sub_part 2: Trade Second CO order via House Fill
        self.trade_entry.set_default_trade(order_id_second, self.price_of_second_order, self.qty_of_second_order)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'SourceAccountID': self.source_acc})
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        execution_second_order = \
            self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value, ).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_second_order[JavaApiFields.ExecID.value]
        # end_of_sub_part
        # end_of_part
        # endregion

        # region step 1: Get position from account
        result_of_position_for_security_account = self._extract_cum_values_for_account(self.source_acc)
        # endregion

        # region step 2: Get position for washbook
        result_of_position_for_washbook = self._extract_cum_values_for_account(self.wash_book)
        # endregion

        # region step 3-4: Amend execution ,which was done via house_fill
        self.trade_entry.get_parameters().clear()
        new_qty = '70'
        self.trade_entry.set_default_amend_house_fill(order_id_second, new_qty, self.price_of_second_order,
                                                      self.source_acc, exec_id)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        wash_book_posit_request = \
            self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, self.wash_book).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        security_account_posit_request = \
            self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, self.source_acc).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        # endregion

        # region step 5: Check PositQty of security account
        decreased_qty = str(float(self.qty_of_second_order) - float(new_qty))
        posit_qty_before = result_of_position_for_security_account[JavaApiFields.PositQty.value]
        posit_qty_after = security_account_posit_request[JavaApiFields.PositQty.value]
        self.ja_manager.compare_values({'DecreasingQty': decreased_qty},
                                       {'DecreasingQty': str(float(posit_qty_after) - float(posit_qty_before))},
                                       f'Verifying that {JavaApiFields.PositQty.value} increased by 30 for {self.source_acc} (step 5)')

        # endregion

        # region step 6: Check PositQty of washbook
        posit_qty_before = result_of_position_for_washbook[JavaApiFields.PositQty.value]
        posit_qty_after = wash_book_posit_request[JavaApiFields.PositQty.value]
        self.ja_manager.compare_values({'DecreasingQty': decreased_qty},
                                       {'DecreasingQty': str(float(posit_qty_before) - float(posit_qty_after))},
                                       f'Verifying that {JavaApiFields.PositQty.value} decreased by 30 for {self.wash_book} (step 6)')
        # endregion

    def _create_orders(self, dictionary_with_needed_tags):
        self.order_submit.get_parameters().clear()
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
