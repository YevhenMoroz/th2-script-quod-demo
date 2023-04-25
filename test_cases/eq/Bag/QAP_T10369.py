import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    SubmitRequestConst, ExecutionReportConst
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
class QAP_T10369(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
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
        self.unmatch_request = UnMatchRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {"AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id1 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {"ClOrdID": bca.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id1, ord_id2]
        basket_name = 'Basket_for_QAP_T10369'
        self.create_basket.set_default(orders_id, basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_basket)
        list_notification = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.OrderListName.value: basket_name}, list_notification,
                                             'Check created basket (step 1)')
        list_id = list_notification[JavaApiFields.OrderListID.value]
        # endregion

        # region Step 2
        bag_name = 'Bag_for_QAP_T10369'
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id)
        self.bag_creation_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameter(
                JavaApiFields.OrderBagNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}, order_bag_notification,
            'Check Bag Status after Bag creation')
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]

        # region check first order
        ord_notif1 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id1).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagID.value: bag_order_id}, ord_notif1,
            "Check OrderBagID in the 1 Order (step 2)")

        # region check second order
        ord_notif2 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id2).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagID.value: bag_order_id}, ord_notif2,
            "Check OrderBagID in the 2 Order (step 2)")
        # endregion

        # region Step 3
        nos_rule = None
        self.basket_wave.set_default(list_id, orders_id)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic,
                                                                                          int(self.price),
                                                                                          int(self.qty),
                                                                                          0)
            self.java_api_manager.send_message_and_receive_response(self.basket_wave)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check first order
        exec_report1 = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                              ord_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report1,
            'Check 1 Care order after execution (step 3)')
        exec_id1 = exec_report1[JavaApiFields.ExecID.value]

        # region check second order
        exec_report2 = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                              ord_id2).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report2,
            'Check 2 Care order after execution (step 3)')

        # region Step 5
        self.dissociate_request.set_default(bag_order_id)
        self.java_api_manager.send_message_and_receive_response(self.dissociate_request)

        # region check first order
        ord_notif1 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                            ord_id1).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdNotificationBlock.value: JavaApiFields.OrderBagID.value}, ord_notif1,
            "Check OrderBagID is absent in the 1 Order (step 5)", VerificationMethod.NOT_CONTAINS)

        # region check second order
        ord_notif2 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                            ord_id2).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdNotificationBlock.value: JavaApiFields.OrderBagID.value}, ord_notif2,
            "Check OrderBagID is absent in the 2 Order (step 5)", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region Step 6
        self.unmatch_request.set_default(self.data_set, exec_id1)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ord_id1).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
             JavaApiFields.LeavesQty.value: self.qty + '.0'}, exec_report,
            'Check Care order after unmatch action (step 6)')
        # endregion