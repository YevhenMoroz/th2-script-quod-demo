import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7063(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.accept_request = CDOrdAckBatchRequest()
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.client = self.data_set.get_client_by_name('client_2')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.responses = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition : Create CO order , accept its and split its

        # part 1: Create and Accept CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.new_order_single.set_default_care_limit()
        self.new_order_single.update_fields_in_component('NewOrderSingleBlock', {'ClientAccountGroupID': self.client})
        qty = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.OrdQty.value]
        price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        self.java_api_manager2.send_message_and_receive_response(self.new_order_single)
        cd_ord_notif = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # end of part

        # part 2: Split CO order
        listing = self.data_set.get_listing_id_by_name("listing_3")
        instrument = self.data_set.get_instrument_id_by_name("instrument_2")
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.exec_destination,
                float(price))
            self.order_submit.set_default_child_dma(order_id)
            route_params = {'RouteBlock': [{'RouteID': self.data_set.get_route_id_by_name("route_1")}]}
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': qty,
                                                                                 'ExecutionPolicy': ExecutionPolicyConst.DMA.value,
                                                                                 'RouteList': route_params,
                                                                                 'InstrID': instrument,
                                                                                 'AccountGroupID': self.client,
                                                                                 'ListingList': {'ListingBlock':
                                                                                     [{
                                                                                         'ListingID': listing}]}
                                                                                 })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_ord_id = order_reply[JavaApiFields.OrdID.value]
            child_cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                 JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value}, order_reply,
                'Verifying that Child DMA order created (step 2)')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule)
            # end of part

        # endregion

        # region step 1: send Fix_OrderCancelRequest
        self.cancel_request.set_default_cancel(cl_ord_id)
        self.java_api_manager2.send_message_and_receive_response(self.cancel_request)
        # endregion

        # region step 2: Accept and cancel children
        cd_ord_notif_message = \
            self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
                [JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, 'C')
        self.accept_request.update_fields_in_component('CDOrdAckBatchRequestBlock', {'CancelChildren': 'Y'})
        self.java_api_manager.send_message_and_receive_response(self.accept_request,
                                                                {order_id: order_id, child_ord_id: child_ord_id})
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecType_PCA.value},
                                             order_reply, 'Verifying that Parent order has PCA status')
        # endregion
