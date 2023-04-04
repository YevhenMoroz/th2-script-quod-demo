import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    SubmitRequestConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationRequest import \
    OrderBagWaveModificationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10328(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty2 = '300'
        self.qty1 = '200'
        self.qty_create_order_1 = '150'
        self.qty_create_order_2 = '100'
        self.qty_create_order_3 = '250'
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.bag_mod_req = OrderBagWaveModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {'OrdQty': self.qty1})
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {'OrdQty': self.qty2, "ClOrdID": bca.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id, ord_id2]
        bag_name = 'QAP_T10329'

        # region Step 2
        self.bag_creation_request.set_default(BagChildCreationPolicy.First_to_Last.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameter(
                JavaApiFields.OrderBagNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}, order_bag_notification,
            'Check Bag Status after Bag creation')
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        # endregion

        # region Step 3-4
        sliced_ord_id_1 = self.__create_order_action(bag_order_id, self.qty_create_order_1)

        # region check orders sts after trade
        # first CO
        self.__check_order_sts(ord_id, ExecutionReportConst.TransExecStatus_PFL.value, self.qty_create_order_1 + '.0', 4)

        # second CO
        exec_for_order_2 = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value,
                                                                  ord_id2).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.CumQty.value: '0.0'}, exec_for_order_2,
            'Check second CO after sliced order trade (step 4)')

        # sliced order
        self.__check_order_sts(sliced_ord_id_1, ExecutionReportConst.TransExecStatus_FIL.value,
                               self.qty_create_order_1 + '.0', 4)
        # endregion

        # region Step 5-6
        sliced_ord_id_2 = self.__create_order_action(bag_order_id, self.qty_create_order_2)

        # region check orders sts after trade
        # first CO
        self.__check_order_sts(ord_id, ExecutionReportConst.TransExecStatus_FIL.value, self.qty1 + '.0', 6)

        # second CO
        self.__check_order_sts(ord_id2, ExecutionReportConst.TransExecStatus_PFL.value, '50.0', 6)

        # sliced order
        self.__check_order_sts(sliced_ord_id_2, ExecutionReportConst.TransExecStatus_FIL.value,
                               self.qty_create_order_2 + '.0', 6)
        # endregion

        # region Step 7-8
        sliced_ord_id_3 = self.__create_order_action(bag_order_id, self.qty_create_order_3)

        # region check orders sts after trade
        # first CO
        self.__check_order_sts(ord_id2, ExecutionReportConst.TransExecStatus_FIL.value, self.qty2 + '.0', 8)

        # sliced order
        self.__check_order_sts(sliced_ord_id_3, ExecutionReportConst.TransExecStatus_FIL.value,
                               self.qty_create_order_3 + '.0', 8)
        # endregion

    def __create_order_action(self, bag_order_id, qty):
        self.order_submit2.set_default_dma_limit()
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {'OrdQty': qty,
                                                                              'AvgPriceType': "BA",
                                                                              'ExternalCare': 'N',
                                                                              "SlicedOrderBagID": bag_order_id,
                                                                              "ClOrdID": bca.client_orderid(9)})
        slice_order_id = None
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic,
                                                                                          int(self.price),
                                                                                          int(qty),
                                                                                          0)
            self.java_api_manager.send_message_and_receive_response(self.order_submit2)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id = order_reply[JavaApiFields.OrdID.value]
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        return slice_order_id

    def __check_order_sts(self, order_id, sts, cum_qty, step):
        exec_for_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                order_id).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: sts,
             JavaApiFields.CumQty.value: cum_qty}, exec_for_order,
            f'Check {sts} for {order_id} after sliced order trade (step {step})')
