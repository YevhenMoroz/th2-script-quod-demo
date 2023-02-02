import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7632(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region check order open status
        self.order_submit.set_default_child_dma(order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'Price': str(int(self.price) + 5),
                                                                             'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                 "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        self.java_api_manager.compare_values({
                                                 'FreeNotes': '11605 \'Price\' (25) greater than Parent\'s \'Price\' (20) / \'Price\' (25) greater than Parent\'s \'Price\' (20)'},
                                             ord_notify_block, 'Check Error message')
        # endregion
