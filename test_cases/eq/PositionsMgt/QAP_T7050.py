import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes, ExecutionReportConst, AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7050(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.source_acc = self.data_set.get_account_by_name("client_pos_3_acc_2")
        self.source_acc_second = self.data_set.get_account_by_name("client_pos_3_acc_4")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.accept_request = CDOrdAckBatchRequest()
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.last_mkt = "BAML"
        self.manual_cross_request = ManualOrderCrossRequest()
        self.request_for_position = RequestForPositions()
        self.listing_id = self.data_set.get_listing_id_by_name('listing_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set client commission to CO orders and create them:

        # part 1: Set Client Commission via WebAdmin
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile,
                                                                         client=self.client)
        self.rest_commission_sender.send_post_request()
        # end_of_part

        # part 2: Create CO orders
        order_id_first = self._create_orders(self.source_acc, SubmitRequestConst.Side_Buy.value)
        order_id_second = self._create_orders(self.source_acc_second, SubmitRequestConst.Side_Sell.value)
        result_for_first_account = self._extract_cum_values_for_account(self.source_acc)
        result_for_second_account = self._extract_cum_values_for_account(self.source_acc_second)
        cum_buy_qty_before = result_for_first_account[JavaApiFields.CumBuyQty.value].replace(',', '')
        cum_sell_qty_before = result_for_second_account[JavaApiFields.CumSellQty.value].replace(',', '')
        # end_of_part

        # endregion

        # region step 1: Manual Cross CO orders
        self.manual_cross_request.set_default(self.data_set, order_id_first,
                                              order_id_second, self.price, self.qty)
        self.manual_cross_request.update_fields_in_component('ManualOrderCrossRequestBlock', {'LastMkt': self.last_mkt,
                                                                                              'ListingID': self.listing_id})
        self.ja_manager.send_message_and_receive_response(self.manual_cross_request)
        execution_report_first = \
            self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id_first).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        execution_report_second = \
            self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id_second).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        position_report_for_first_account = \
            self.ja_manager.get_last_message(PKSMessageType.PositionReport.value, self.source_acc).get_parameters()[
                JavaApiFields.PositionReportBlock.value]
        position_report_for_second_account = \
            self.ja_manager.get_last_message(PKSMessageType.PositionReport.value, self.source_acc_second).get_parameters()[
                JavaApiFields.PositionReportBlock.value]
        list_execuiton_report = [execution_report_first, execution_report_second]
        for message in list_execuiton_report:
            self.ja_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                message, f'Verifying that {message[JavaApiFields.OrdID.value]} is filled (step 1)')
        # endregion

        # region step 2: Check that CO orders have Client Commission
        currency = self.data_set.get_currency_by_name('currency_2')
        commission_rate = str(float(5))
        commission_amount = str((float(self.qty) * float(self.price)) / 10000 * float(commission_rate))
        expected_client_commission = {'ClientCommissionBlock': [{'CommissionAmount': commission_amount,
                                                                 'CommissionAmountSubType': AllocationInstructionConst.CommissionAmountSubType_OTH.value,
                                                                 'CommissionAmountType': AllocationInstructionConst.CommissionAmountType_BRK.value,
                                                                 'CommissionBasis': AllocationInstructionConst.COMM_AND_FEE_BASIS_PCT.value,
                                                                 'CommissionCurrency': currency,
                                                                 'CommissionRate': commission_rate}]}
        for message in list_execuiton_report:
            self.ja_manager.compare_values(
                expected_client_commission,
                message[JavaApiFields.ClientCommissionList.value],
                f'Verifying that {message[JavaApiFields.OrdID.value]} has client commission (step 2)')
        # endregion

        # region step 3: Check that CumBuyQty changes for first account, CumSellQty for second
        cum_buy_qty_after = \
            position_report_for_first_account[JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value][0][
                JavaApiFields.CumBuyQty.value]
        cum_sell_qty_after = \
            position_report_for_second_account[JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value][0][
                JavaApiFields.CumSellQty.value]
        self.ja_manager.compare_values({'IncreasingBuyQty': str(float(self.qty)), 'IncreasingSellQty': str(float(self.qty))},
                                       {'IncreasingBuyQty': str(float(cum_buy_qty_after) - float(cum_buy_qty_before)),
                                        'IncreasingSellQty': str(
                                            float(cum_sell_qty_after) - float(cum_sell_qty_before))},
                                       f'Verifying that {JavaApiFields.CumBuyQty.value} for {self.source_acc} and '
                                       f'{JavaApiFields.CumSellQty.value} increased on {self.qty} (step 3)')
        # endregion

    def _create_orders(self, alloc_account, side):
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {
            "InstrID": self.instrument_id,
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            "PreTradeAllocationBlock": {
                "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                    {"AllocAccountID": alloc_account, "AllocQty": self.qty}]}},
            'Side': side,
            "AccountGroupID": self.client,
            "ClOrdID": bca.client_orderid(9)})
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
