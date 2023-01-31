import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7414(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price_of_orders = '10'
        price_of_wave = '2'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price_of_orders)
        qty_of_bag = float(qty) * 2
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        name_of_bag = 'QAP_T7414'
        new_order_single_rule = trade_rule = None

        # endregion

        # region precondition : create 2 CO order via FIX
        order_ids = []
        cl_ord_ids = []
        for i in range(2):
            self.fix_message.change_parameter('ClOrdID', bca.client_orderid(9))
            responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            response = responses[0]
            order_ids.append(response.get_parameters()['OrderID'])
            cl_ord_ids.append(response.get_parameters()['ClOrdID'])
        # endregion

        # region step 1, step 2, step 3, step 4: Create BagOrder
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, name_of_bag, order_ids)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (step 4)')
        # endregion

        # region step 5: Create Wave and execute its
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {
            "Price": price_of_wave
        })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, client_for_rule, exec_destination, float(price_of_wave))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            exec_destination,
                                                                                            float(price_of_wave),
                                                                                            int(qty), 0)

            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
            order_bag_wave_notification = \
                self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value).get_parameters()[
                    JavaApiFields.OrderBagWaveNotificationBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderWaveStatus_TER.value},
                order_bag_wave_notification,
                'Checking that wave terminated (step 5)')
        except Exception as E:
            logger.error(f'{E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 6: Check Execution report on sell side
        list_of_ignored_fields = ['Account', 'ReplyReceivedTime',
                                  'SettlCurrency', 'SecondaryOrderID',
                                  'LastMkt']
        for cl_ord_id in cl_ord_ids:
            self.fix_message.change_parameter('ClOrdID', cl_ord_id)
            self.execution_report.set_default_filled(self.fix_message)
            self.execution_report.change_parameter('AvgPx', price_of_wave)
            self.fix_verifier.check_fix_message_fix_standard(self.execution_report, ignored_fields=list_of_ignored_fields)
        # endregion
