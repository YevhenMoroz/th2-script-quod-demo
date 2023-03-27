import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, PKSMessageType, ORSMessageType
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
class QAP_T7579(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.firm_client = self.data_set.get_client_by_name("client_pos_3")
        self.firm_acc = self.data_set.get_account_by_name("client_pos_3_acc_3")
        self.wb_client = self.data_set.get_client_by_name('client_pos_1')
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.price_for_firm_and_washbook = '10'
        self.qty_for_wash_book = '100.0'
        self.qty_for_firm = '200.0'
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.request_for_position = RequestForPositions()
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set client commission to CO orders and create them:
        # part 1: Create CO orders
        orders_id_list = []
        variable_parameters = [{
            'OrdQty': self.qty_for_firm,
            "PreTradeAllocationBlock": {
                "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                    {"AllocAccountID": self.firm_acc, "AllocQty": self.qty_for_firm}]}},
            "AccountGroupID": self.firm_client,
            'Price': self.price_for_firm_and_washbook,
            "ClOrdID": bca.client_orderid(9)}, {'OrdQty': self.qty_for_wash_book, "AccountGroupID": self.wb_client,
                                                'Price': self.price_for_firm_and_washbook,
                                                "ClOrdID": bca.client_orderid(9),
                                                'WashBookAccountID': self.wash_book}]
        for parameters in variable_parameters:
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.desk,
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', parameters)
            orders_id_list.append(self._create_order(self.order_submit))
            self.order_submit.get_parameters().clear()
        # end_of_part

        # part 2: Perform Manual Execute and House Fill
        self.trade_entry_request.set_default_trade(orders_id_list[0], exec_qty=self.qty_for_firm)
        self.ja_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_firm_account = execution_report[JavaApiFields.ExecID.value]
        self.trade_entry_request.set_default_house_fill(orders_id_list[1], self.firm_acc,
                                                        exec_qty=self.qty_for_wash_book)
        self.ja_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_washbook = execution_report[JavaApiFields.ExecID.value]
        # end_of_part

        # region step 1 -2 : Get Position for washBook and firm_account
        wash_book_position = self._extract_position(self.wash_book)
        firm_account_position = self._extract_position(self.firm_acc)
        # endregion

        # region step 3: Cancel House Fill
        self.trade_entry_request.set_default_cancel_house_fill(orders_id_list[1], self.firm_acc, exec_id_washbook)
        self.ja_manager.send_message_and_receive_response(self.trade_entry_request, response_time=14000)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.ja_manager.compare_values({JavaApiFields.LeavesQty.value: self.qty_for_wash_book},
                                       order_reply,
                                       f"Verifing that second CO order has {JavaApiFields.LeavesQty.value} as {self.qty_for_wash_book} (step 3)")
        # endregion

        # region step 4: Check that position of firm account decreased
        position_report_firm = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                   [self.firm_acc,
                                                                                    JavaApiFields.PositQty.value]). \
            get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        cumm_sell_qty_of_firm_acc_before_chf = firm_account_position[JavaApiFields.CumSellQty.value]
        cumm_sell_qty_of_firm_acc_after_chf = position_report_firm[JavaApiFields.CumSellQty.value]
        expected_decreased_qty = str(float(cumm_sell_qty_of_firm_acc_before_chf) - float(cumm_sell_qty_of_firm_acc_after_chf))
        self.ja_manager.compare_values({'DecreasedCummSellQty': self.qty_for_wash_book},
                                       {'DecreasedCummSellQty': expected_decreased_qty},
                                       f'Verifying that {JavaApiFields.CumSellQty.value} of Firm Account decreased on {self.qty_for_wash_book} (step 4)')
        # endregion

        # region step 5: Check  that position of washbook decreased
        position_report_washbook = \
        self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                            [self.wash_book,
                                                             JavaApiFields.PositQty.value]). \
            get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        cumm_buy_qty_of_washbook_before_chf = wash_book_position[JavaApiFields.CumBuyQty.value]
        cumm_buy_qty_of_washbook_after_chf = position_report_washbook[JavaApiFields.CumBuyQty.value]
        expected_decreased_qty = str(float(cumm_buy_qty_of_washbook_before_chf) - float(cumm_buy_qty_of_washbook_after_chf))
        self.ja_manager.compare_values({'DecreasedCummBuyQty': self.qty_for_wash_book},
                                       {'DecreasedCummBuyQty': expected_decreased_qty},
                                       f'Verifying that {JavaApiFields.CumBuyQty.value} of Washbook decreased on {self.qty_for_wash_book} (step 5)')
        # endregion

        # region step 6: Cancel Manual Execution of First Order
        self.trade_entry_request.get_parameters().clear()
        self.trade_entry_request.set_default_cancel_execution(orders_id_list[0], exec_id_firm_account)
        self.ja_manager.send_message_and_receive_response(self.trade_entry_request)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.ja_manager.compare_values({JavaApiFields.LeavesQty.value: self.qty_for_firm},
                                       order_reply,
                                       f"Verifing that first CO order has {JavaApiFields.LeavesQty.value} as {self.qty_for_firm} (step 6)")
        # endregion

        # region step 7: Check position of firm account
        position_report_firm_second = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                   [self.firm_acc,
                                                                                    JavaApiFields.PositQty.value]). \
            get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        cumm_buy_qty_of_firm_acc_before_ce = position_report_firm[JavaApiFields.CumBuyQty.value]
        cumm_buy_qty_of_firm_acc_after_ce = position_report_firm_second[JavaApiFields.CumBuyQty.value]
        expected_decreased_qty = str(
            float(cumm_buy_qty_of_firm_acc_before_ce) - float(cumm_buy_qty_of_firm_acc_after_ce))
        self.ja_manager.compare_values({'DecreasedCummBuyQty': self.qty_for_firm},
                                       {'DecreasedCummBuyQty': expected_decreased_qty},
                                       f'Verifying that {JavaApiFields.CumBuyQty.value} of Firm Account decreased on {self.qty_for_firm} (step 7)')
        # endregion



    def _create_order(self, order_submit):
        self.ja_manager_second.send_message_and_receive_response(order_submit)
        cd_ord_notif = self.ja_manager_second.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, self.desk)
        self.ja_manager.send_message_and_receive_response(self.accept_request)
        return order_id

    def _extract_position(self, account):
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
