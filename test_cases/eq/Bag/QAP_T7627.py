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
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7627(TestCase):
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
        self.ord_mod = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        resp = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)
        ord_id = resp[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        orders_id = [ord_id, ord_id2]
        # endregion
        # region Step 1-2
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        new_qty = str(int(int(self.qty) * 2))
        # endregion
        # region Step 3
        self.ord_mod.set_default(self.data_set, ord_id)
        self.ord_mod.update_fields_in_component("OrderModificationRequestBlock", {"OrdQty": new_qty})
        self.java_api_manager.send_message_and_receive_response(self.ord_mod)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        qty_of_bag = str(float(self.qty) * 3)
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           JavaApiFields.OrderBagQty.value: qty_of_bag}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, "Check Bag")
        # endregion
