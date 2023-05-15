import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    BasketMessagesConst, OrdListNotificationConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderListOMS import FixNewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCancelRequest import OrderListWaveCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest
from test_framework.fix_wrappers import DataSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()

class QAP_T7365(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier_bs = FixVerifier(self.bs_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_orderlist_submit = FixNewOrderListOMS(self.data_set)
        self.price = '10'
        self.qty = '100'
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.create_wave_request = OrderListWaveCreationRequest()
        self.cancel_wave_request = OrderListWaveCancelRequest()
        self.remove_orders_from_order_list_request = RemoveOrdersFromOrderListRequest()
        self.instrument_1 = self.data_set.get_java_api_instrument("instrument_1")
        self.basket_name = 'QAP_T7365'
        self.create_order_list_from_existing_orders_request = NewOrderListFromExistingOrders()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create Basket
        self.fix_orderlist_submit.set_default_order_list()
        self.fix_orderlist_submit.base_parameters['NewOrderListBlock']["NewOrderListElements"]["NewOrderSingleBlock"][1]["Side"]='Buy'
        self.java_api_manager.send_message_and_receive_response(self.fix_orderlist_submit, response_time=5000)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value
        ).get_parameter(JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            list_notify_block,
            "Step 1 - Checking Status for created Basket",
        )
        order_list_id = list_notify_block["OrderListID"]
        ord_id1 = list_notify_block["OrdNotificationElements"]["OrdNotificationBlock"][0]["OrdID"]
        ord_id2 = list_notify_block["OrdNotificationElements"]["OrdNotificationBlock"][1]["OrdID"]
        # endregion

        # regin Step 2 - Wave Basket
        self.create_wave_request.set_default(order_list_id, [ord_id1, ord_id2])
        route_params = {"RouteID": self.route_id}
        self.create_wave_request.update_fields_in_component('OrderListWaveCreationRequestBlock', route_params)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.java_api_manager.send_message_and_receive_response(self.create_wave_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        list_wave_notif = self.java_api_manager.get_last_message(ORSMessageType.OrderListWaveNotification.value)
        wave_notif_block = list_wave_notif.get_parameter(JavaApiFields.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_NEW.value,
             JavaApiFields.PercentQtyToRelease.value: '1.0', JavaApiFields.RouteID.value: str(self.route_id)}, {
                JavaApiFields.OrderListWaveStatus.value:
                    wave_notif_block[
                        JavaApiFields.OrderListWaveStatus.value],
                JavaApiFields.PercentQtyToRelease.value:
                    wave_notif_block[
                        JavaApiFields.PercentQtyToRelease.value], JavaApiFields.RouteID.value: wave_notif_block[
                    JavaApiFields.RouteID.value]},
            "Step 2 - Check Wave values")
        wave_id = wave_notif_block['OrderListWaveID']
        ch_orders_id = []
        ch_orders_id.append(wave_notif_block[JavaApiFields.OrderNotificationElements.value][
            JavaApiFields.OrderNotificationBlock.value][0]['OrdID'])
        ch_orders_id.append(wave_notif_block[JavaApiFields.OrderNotificationElements.value][
            JavaApiFields.OrderNotificationBlock.value][1]['OrdID'])
        # endregion

        # region Step 3 and Step 4 - Cancel Wave
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest(self.bs_connectivity, self.rule_client,
                                                                   self.mic, True)
            self.cancel_wave_request.set_default(wave_id)
            self.java_api_manager.send_message_and_receive_response(self.cancel_wave_request)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        change_parameters1 = {
            'OrigClOrdID': ch_orders_id[0],
        }
        change_parameters2 = {
            'OrigClOrdID': ch_orders_id[1],
        }
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
                                  'SettlCurrency', 'StrategyName', 'ClOrdID'
                                  ]
        execution_report1 = FixMessageExecutionReportOMS(self.data_set, change_parameters1)
        execution_report2 = FixMessageExecutionReportOMS(self.data_set, change_parameters2)
        execution_report1.change_parameters({'ExecType': '4', "OrdStatus": "4"})
        execution_report2.change_parameters({'ExecType': '4', "OrdStatus": "4"})
        self.fix_verifier_bs.check_fix_message_fix_standard(execution_report1, ['OrigClOrdID', 'ExecType'], ignored_fields=list_of_ignored_fields, direction=DataSet.DirectionEnum.ToQuod)
        self.fix_verifier_bs.check_fix_message_fix_standard(execution_report2, ['OrigClOrdID', 'ExecType'], ignored_fields=list_of_ignored_fields, direction=DataSet.DirectionEnum.ToQuod)
        # endregion

        # region - Step 5 - Remove orders from Basket
        list_of_orders = [ord_id1, ord_id2]
        order_list = []
        for order_id in list_of_orders:
            order_id_dict = {"OrdID": order_id}
            order_list.append(order_id_dict)
        self.remove_orders_from_order_list_request.set_default(ord_id1, order_list_id)
        self.remove_orders_from_order_list_request.update_fields_in_component('RemoveOrdersFromOrderListRequestBlock',
                                                                          {"OrdIDList":
                                                                              {
                                                                                  "OrdIDBlock":
                                                                                      order_list
                                                                              }})
        self.java_api_manager.send_message_and_receive_response(self.remove_orders_from_order_list_request)
        ord_list_notify = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_DON.value},
            ord_list_notify, 'Step 5 - Check Basket sts after removing orders')
        # endregion

        # region - Step 6 - create Basket
        self.create_order_list_from_existing_orders_request.set_default(list_of_orders, self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_order_list_from_existing_orders_request)
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
                'NewOrderListReplyBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Step 6 - Check List status')
        # endregion