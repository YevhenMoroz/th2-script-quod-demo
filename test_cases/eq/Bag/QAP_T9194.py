import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    SubmitRequestConst, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9194(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.order_submit3 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.basket_wave = OrderListWaveCreationRequest()
        self.create_basket = NewOrderListFromExistingOrders()
        self.dissociate_request = OrderBagDissociateRequest()
        self.manual_match_request = ManualMatchExecToParentOrdersRequest()
        self.unmatch_request = UnMatchRequest()
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '300'
        price = '20'
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        currency = self.data_set.get_currency_by_name('currency_1')
        # endregion

        # region Step 1  - Create 2 Care Orders
        # subregion Create 1st Care Order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"Side": "Sell",
             "OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id1 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            f'Step 1: Checking 1st CO is created {ord_id1}')

        # subregion Step 1: Create 2nd Care Order
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {"ClOrdID": bca.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id1, ord_id2]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            f'Step 1: Checking 2nd CO is created {ord_id1}')
        # endregion

        # region Step 2: Create Basket
        basket_name = 'Basket_for_QAP_T10369'
        self.create_basket.set_default(orders_id, basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_basket)
        list_notification = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.OrderListName.value: basket_name}, list_notification,
                                             'Step 2: Checking created basket')
        list_id = list_notification[JavaApiFields.OrderListID.value]
        # endregion

        # region Step 3: Create Bag
        orders_id = [ord_id1, ord_id2]
        bag_name = 'QAP_T9194'

        self.bag_creation_request.set_default(BagChildCreationPolicy.Group.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: bag_name,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Step 3: Checking bag is created')
        # endregion

        # region Step 4: Create Care Order from Bag
        client_ord_id1 = bca.client_orderid(9)
        slice_order_id1 = None
        self.order_submit2.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=self.desk, role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit2.update_fields_in_component('NewOrderSingleBlock',
                                                      {
                                                          "Side": "Sell",
                                                          'SlicedOrderBagID': bag_order_id,
                                                          'OrdQty': qty,
                                                          "AccountGroupID": client,
                                                          "Price": '5',
                                                          'ClOrdID': client_ord_id1,
                                                          'AvgPriceType': "BA",
                                                          "SpecialDeal": "N",
                                                          "ExternalCare": "N"
                                                      })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, venue_client_account, exec_destination, float(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit2)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id1). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id1 = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Step 4: Checking that Slice Care order is created')
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region Step 5: Create DMA Order and execute it
        # subregion Step 5: Create DMA
        client_ord_id2 = bca.client_orderid(9)
        slice_order_id2 = None
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         'Side': 'Sell',
                                                         'OrdQty': qty,
                                                         "Price": '5',
                                                         'ClOrdID': client_ord_id2
                                                     })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, venue_client_account, exec_destination, float(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id2). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id2 = order_reply[JavaApiFields.OrdID.value]
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)

        # subregion Step 5: Execute DMA
        self.execution_report.set_default_trade(slice_order_id2)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "OrdQty": qty,
            "LastTradedQty": qty,
            "LastPx": '5',
            "Price": '5',
            "LeavesQty": '0',
            "CumQty": qty,
            "AvgPrice": '5'})
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Step 5: Verifying that DMA order is filled')
        # endregion

        # region Step 6: Manual Match for DMA execution
        # subregion Step6: Match
        self.manual_match_request.set_default(slice_order_id1, qty, exec_id)
        self.java_api_manager.send_message_and_receive_response(self.manual_match_request)

        # subregion Step 6: verifying values of care order after match
        exec_report_block = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, exec_report_block,
            'Step 6: Comparing values for 1st Care order (after match)')
        exec_report_block = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id2).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, exec_report_block,
            'Step 6: Comparing values for 2nd Care order (after match)')
        exec_report_block = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, slice_order_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id = exec_report_block[JavaApiFields.ExecID.value]
        # endregion

        # region Step 7: Unmatch for Care Order
        # subregion Step 7: Unmatch
        self.unmatch_request.set_default(self.data_set, exec_id, qty)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)

        # subregion Step 7: Verify orders' fields after unmatch
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             slice_order_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
             JavaApiFields.LeavesQty.value: qty + '.0'}, exec_report,
            'Step 7: Check Sliced Care order after unmatch action')
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ord_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
             JavaApiFields.LeavesQty.value: qty + '.0'}, exec_report,
            'Step 7: Check 1st Care order after unmatch action')
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ord_id2).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
             JavaApiFields.LeavesQty.value: qty + '.0'}, exec_report,
            'Step 7: Check 2nd Care order after unmatch action')
        # endregion