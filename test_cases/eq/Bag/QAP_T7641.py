import logging
import os
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveCancelRequest import OrderBagWaveCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7641(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.nos.get_parameter("Price")
        self.qty = self.nos.get_parameter("OrderQtyData")["OrderQty"]
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.wave_cancel_request = OrderBagWaveCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        resp = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)

        ord_id = resp[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        orders_id = [ord_id, ord_id2]
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
                self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        qty_of_bag = str(int(int(self.qty) * 2))
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
                .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        wave_id = wave_notify["OrderBagWaveID"]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Check wave from precondition")
        # endregion
        # region Step 1-3
        self.wave_cancel_request.set_default(wave_id)
        try:
            nos_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity, self.venue_client_name
                                                                            , self.mic, True)
            self.java_api_manager.send_message_and_receive_response(self.wave_cancel_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value, ord_id).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        ord_update2 = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value, ord_id2).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        expected_result = {"UnmatchedQty": str(float(self.qty))}
        self.java_api_manager.compare_values(expected_result, ord_update, "UnmatchedQty for order 1")
        self.java_api_manager.compare_values(expected_result, ord_update2, "UnmatchedQty for order 2")
        # endregion
