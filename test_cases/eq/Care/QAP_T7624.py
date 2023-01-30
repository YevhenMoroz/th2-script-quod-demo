import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, TimeInForces, OrdTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7624(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.price = self.fix_message.get_parameter('Price')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        # endregion

        # region DirectLOC with qty = 0
        self.order_submit.set_default_child_dma(order_id, cl_ord_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'ListingList': {'ListingBlock': [
                                                         {
                                                             'ListingID': self.data_set.get_listing_id_by_name(
                                                                 "listing_3")}]},
                                                         'InstrID': self.data_set.get_instrument_id_by_name(
                                                             "instrument_2"),
                                                         'Price': self.price,
                                                         'OrdQty': self.qty, 'TimeInForce': self.data_set.get_time_in_force(
                                                         'time_in_force_3')
                                                     })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # region check values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({
            JavaApiFields.OrdQty.value: self.qty + '.0',
            JavaApiFields.TimeInForce.value: TimeInForces.ATC.value, JavaApiFields.OrdType.value: OrdTypes.Limit.value},
            ord_reply_block, "Check error values after Direct LOC")
        # endregion