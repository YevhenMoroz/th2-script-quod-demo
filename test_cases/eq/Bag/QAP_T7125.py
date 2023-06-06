import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    BagChildCreationPolicy, ExecutionReportConst, OrderBagConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7125(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.order_slice = OrderSubmitOMS(data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.bag_modification_request = ModifyBagOrderRequest()
        self.bag_dissociate_request = OrderBagDissociateRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        half_qty = str(int(qty) / 2)
        orders_id = []
        name_of_bag = 'QAP_T7125'
        last_bag_order_qty = str(float(qty) * 3)
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_client_by_name('client_pt_1')
        currency = self.data_set.get_currency_by_name('currency_1')
        # endregion

        # region Step 1: Create 3 CO orders
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        for counter in range(3):
            self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                         {
                                                             "ClOrdID": bca.client_orderid(9)
                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)

            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            orders_id.append(order_reply[JavaApiFields.OrdID.value])

            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply,
                f'Step 1: Checking {counter+1} CO is created {orders_id[counter]}')
        # endregion

        # region Step 2: Create Bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}

        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Step 2: Checking new Bag is created')
        # endregion

        # region Step 3-4: Create SliceOrder from bag
        client_ord_id = bca.client_orderid(9)
        slice_order_id1 = None
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         'Price': price,
                                                         "AccountGroupID": client,
                                                         'ExecutionPolicy': 'DMA',
                                                         'AvgPriceType': "EA",
                                                         'ExternalCare': 'N',
                                                         'SlicedOrderBagID': bag_order_id,
                                                         'OrdQty': qty,
                                                         'ClOrdID': client_ord_id
                                                     })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, venue_client_account, exec_destination, int(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id1 = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Step 3-4: Checking that Slice order is created')
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region Step 5: Execute Slice order of bag
        filter_dict = {slice_order_id1: slice_order_id1}
        for co_order_id in orders_id:
            filter_dict.update({co_order_id: co_order_id})
        exec_qty = qty
        self.execution_report.set_default_trade(slice_order_id1)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "LastTradedQty": exec_qty,
                                                             "LastPx": price,
                                                             "OrdType": "Limit",
                                                             "Price": price,
                                                             "Currency": currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": '0',
                                                             "CumQty": exec_qty,
                                                             "AvgPrice": price,
                                                             "LastMkt": exec_destination,
                                                             "OrdQty": exec_qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict)

        execution_report_of_slice_order = \
        self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                               filter_dict[slice_order_id1]). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({
            JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value,
            JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value
        }, execution_report_of_slice_order,
            f'Step 5: Checking sliced order after execution {slice_order_id1}')

        for co_order_id in orders_id:
            execution_report_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                               co_order_id). \
                get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
                execution_report_co_order,
                f'Step 5: Checking {co_order_id} CO order after execution')
        # endregion

        # region Step 6: Dissociate Bag
        self.bag_dissociate_request.set_default(bag_order_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_dissociate_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_TER.value},
            order_bag_notification, 'Step 6: Checking OrderBagStatus after Dissociate request')
        # endregion

        # region Step 7: Create 3 CO orders and Bag them
        # subregion Step 7: Create 3 CO orders
        new_orders_id = []
        new_name_of_bag = "new_QAP_T7125"
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        for counter in range(3):
            self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                         {
                                                             "ClOrdID": bca.client_orderid(9)
                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)

            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            new_orders_id.append(order_reply[JavaApiFields.OrdID.value])

            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply,
                f'Step 7: Checking {counter+1} CO is created {new_orders_id[counter]}')

        # subregion Create Bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, new_name_of_bag, new_orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: new_name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}

        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Step 7: Checking new Bag is created')
        # endregion

        # region Step 8: Dissociate Bag
        self.bag_dissociate_request.set_default(bag_order_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_dissociate_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_TER.value},
            order_bag_notification, 'Step 8: Checking OrderBagStatus after Dissociate request')
        # endregion

        # region Step 9: Create Bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, new_name_of_bag, new_orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: new_name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}

        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Step 9: Checking new Bag is created')
        # endregion