import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    BagChildCreationPolicy, OrderBagConst, SubscriptionRequestTypes, PosReqTypes, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10935(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.fe_env = environment.get_list_fe_environment()[0]
        self.user1 = self.fe_env.user_1
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.create_basket_request = NewOrderListFromExistingOrders()
        self.order_modify = OrderModificationRequest()
        self.wash_book_acc = self.data_set.get_washbook_account_by_name('washbook_account_3')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.acc1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.qty1 = '1000'
        self.qty2 = '1500'
        self.name_of_bag = 'Bag_for_QAP_T10935'
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.bag_creation_request = OrderBagCreationRequest()
        self.request_for_position = RequestForPositions()
        self.wave_request = OrderListWaveCreationRequest()
        self.wave_qty = str(int(self.qty1) + int(self.qty2))
        self.price = '5'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region steps 2-3 create care orders:
        order_id1 = self.__create_care_order(self.qty1)
        order_id2 = self.__create_care_order(self.qty2)
        list_of_orders = [order_id1, order_id2]
        # endregion

        # region steps 4 Amend first order:
        pre_trade_dict = {'PreTradeAllocationBlock': {
                                                         'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                             {'AllocAccountID': self.acc1,
                                                              'AllocQty': str(float(self.qty1))}]}}}
        self.order_modify.set_change_params(order_id1)
        self.order_modify.update_fields_in_component('OrderModificationRequestBlock', pre_trade_dict)
        self.java_api_manager.send_message_and_receive_response(self.order_modify)

        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values(pre_trade_dict, ord_reply, 'Check Order after modification')
        # endregion

        # region step 5 create Basket:
        self.create_basket_request.set_default(list_of_orders)
        self.java_api_manager.send_message_and_receive_response(self.create_basket_request)
        list_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        list_id = list_notif[JavaApiFields.OrderListID.value]
        # endregion

        # region create bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, self.name_of_bag, list_of_orders)
        self.bag_creation_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_id = order_bag_notification['OrderBagID']
        expected_result = {JavaApiFields.OrderBagName.value: self.name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Check created bag')
        # endregion

        # region: get position for Security Account CareWB
        posit_qty_before_trade = self._extract_cum_values_for_acc()[JavaApiFields.PositQty.value]

        # region Send wave request
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(self.fix_env.buy_side,
                                                                             self.rule_client,
                                                                             self.mic, True, int(self.wave_qty),
                                                                             float(self.price))
            self.wave_request.set_default(list_id, list_of_orders)
            self.java_api_manager.send_message_and_receive_response(self.wave_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Verify wave
        list_wave_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            JavaApiFields.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrderBagConst.OrderWaveStatus_NEW.value},
            list_wave_notify_block,
            'Check created wave from Bag')
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            'Check child order is filled')
        # endregion

        # region step 9: get position for Security Account CareWB
        posit_qty_after_trade = self._extract_cum_values_for_acc()[JavaApiFields.PositQty.value]
        increment_cum_sell_qty = str(abs(float(posit_qty_after_trade) - float(
            posit_qty_before_trade)))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.PositQty.value}': str(float(self.wave_qty))},
            {f'Increment{JavaApiFields.PositQty.value}': increment_cum_sell_qty},
            f'Verifying that {JavaApiFields.PositQty.value} increased on {self.wave_qty} (step 5)')
        # endregion

    def __create_care_order(self, qty):
        self.order_submit.set_default_care_market(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'WashBookAccountID': self.wash_book_acc,
                                                      "ClOrdID": bca.client_orderid(
                                                          9), 'OrdQty': qty,
                                                      'AccountGroupID': self.client})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        order_id = ord_reply[JavaApiFields.OrdID.value]
        return order_id

    def _extract_cum_values_for_acc(self):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              self.wash_book_acc)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.java_api_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
