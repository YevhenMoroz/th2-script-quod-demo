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
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    BagChildCreationPolicy, OrderBagConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCancelRequest import OrderBagCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7126(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.bag_cancel_request = OrderBagCancelRequest()
        self.trade_entry = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '700'
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        currency = self.data_set.get_currency_by_name('currency_1')
        orders_id = []
        name_of_bag = 'QAP_T7126'
        new_order_single_rule = None
        # endregion

        # region step 1 : Create CO orders
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        for counter in range(2):
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
                f'Checking expected and actually results for {orders_id[counter]} (step 1)')
        # endregion

        # region step 2: Create Bag order
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (step 2)')
        # endregion

        # region step 3 , step 4: Create SliceOrder from bag
        client_ord_id = bca.client_orderid(9)
        slice_order_id = None
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         'ExecutionPolicy': 'DMA',
                                                         'AvgPriceType': "EA",
                                                         'ExternalCare': 'N',
                                                         'SlicedOrderBagID': bag_order_id,
                                                         'OrdQty': qty,
                                                         'ClOrdID': client_ord_id
                                                     })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, venue_client_account, exec_destination, float(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Checking that Slice order created (step 5)')
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region step 5: Execute Slice order of bag
        filter_dict = {slice_order_id: slice_order_id}
        for co_order_id in orders_id:
            filter_dict.update({co_order_id: co_order_id})

        self.execution_report.set_default_trade(slice_order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "LastTradedQty": qty,
                                                             "LastPx": price,
                                                             "OrdType": "Limit",
                                                             "Price": price,
                                                             "Currency": currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": '0',
                                                             "CumQty": qty,
                                                             "AvgPrice": price,
                                                             "LastMkt": exec_destination,
                                                             "OrdQty": qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict)

        execution_report_of_slice_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                                 filter_dict[slice_order_id]). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({
            JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value,
            JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value
        }, execution_report_of_slice_order,
            f'Checking expected and actually result for slicing order {slice_order_id} (step 5)')

        for co_order_id in orders_id:
            execution_report_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                               co_order_id). \
                get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
                execution_report_co_order,
                f'Checking expected and actually result for {co_order_id} CO order (step 5)')
        # endregion

        # region step 6: Cancel Bag
        self.bag_cancel_request.set_default(bag_order_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_cancel_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_CXL.value},
            order_bag_notification, f'Checking {JavaApiFields.OrderBagStatus.value} (step 6)')
        # endregion

        # region step 7
        self.trade_entry.set_default_trade(orders_id[0], price, str(float(qty)/2))
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_report_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).\
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                                             execution_report_co_order,
                                             'Checking expected and actually results (step 7)')
        # endregion
