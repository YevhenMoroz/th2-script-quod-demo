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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, TimeInForces, \
    OrdTypes, PegOffsetTypes, PegScopes
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OffsetTypes
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7634(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_bag_creation = OrderBagCreationRequest()
        self.order_bag_wave_creation = OrderBagWaveRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1101'
        qty_of_bag = str(float(int(qty) * 2))
        price = '10'
        price_offset = '0.05'
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_counterpart_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        client_venue = self.data_set.get_venue_client_names_by_name('client_counterpart_1_venue_1')
        self.fix_message.change_parameter("HandlInst", '3')
        rule_manager = RuleManager(Simulators.equity)
        name_of_bag = 'QAP_T7634'
        order_list = []
        offset_type = OffsetTypes.price.value

        # endregion

        # # region step Precondition
        self.fix_message.change_parameter("HandlInst", '3')
        order_list.append(
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)[0].get_parameter(
                "OrderID"))
        self.fix_message.change_parameter('ClOrdID', bca.client_orderid(9))
        order_list.append(
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)[0].get_parameter(
                "OrderID"))
        self.order_bag_creation.set_default(BagChildCreationPolicy.Split.value, name_of_bag, order_list)
        responses = self.java_api_manager.send_message_and_receive_response(self.order_bag_creation)
        print_message("Creation Bag", responses)
        actually_result = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = actually_result[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag, JavaApiFields.OrderBagQty.value: qty_of_bag}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Comparing values of bag after its creation')
        # endregion

        # region wave bag order (step 1, step 2 and step 3)
        expected_result.clear()
        expected_result.update({JavaApiFields.PegOffsetValue.value: price_offset,
                                JavaApiFields.PegOffsetType.value: PegOffsetTypes.Price.value,
                                JavaApiFields.PegScope.value: PegScopes.Local.value})
        self.order_bag_wave_creation.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value, TimeInForces.DAY.value)
        self.order_bag_wave_creation.update_fields_in_component(JavaApiFields.OrderBagWaveRequestBlock.value, {
            JavaApiFields.PegInstructionsBlock.value: expected_result})

        new_order_single = None
        try:
            new_order_single = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_venue, exec_destination,
                float(price))
            responses = self.java_api_manager.send_message_and_receive_response(self.order_bag_wave_creation)
            print_message('Wave Bag', responses)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            rule_manager.remove_rule(new_order_single)

        # endregion

        # region check Peg value from step 3
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value).\
            get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value][JavaApiFields.PegInstructionsBlock.value]
        self.java_api_manager.compare_values(expected_result, actually_result, 'Comparing values from step 3')
        # endregion
