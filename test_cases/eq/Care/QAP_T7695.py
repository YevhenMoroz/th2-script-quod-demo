import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, TimeInForces, OrderReplyConst, OrdTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7695(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        # endregion

        # region DirectMOC with qty = 0
        self.order_submit.set_default_dma_market()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'ListingList': {'ListingBlock': [
                                                         {
                                                             'ListingID': self.data_set.get_listing_id_by_name(
                                                                 "listing_3")}]},
                                                         'InstrID': self.data_set.get_instrument_id_by_name(
                                                             "instrument_2"),
                                                         'OrdQty': '0', 'TimeInForce': self.data_set.get_time_in_force(
                                                         'time_in_force_3'), "ParentOrdrList": {
                                                         "ParentOrdrBlock": [{"ParentOrdID": order_id}]},
                                                         'ClOrdID': cl_ord_id
                                                     })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # region check values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameter(
            JavaApiFields.NewOrderReplyBlock.value)['Ord']
        self.java_api_manager.compare_values({
            JavaApiFields.FreeNotes.value: '11603 \'OrdQty\' (0) negative or zero / \'OrdQty\' (0) negative or zero',
            JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value,
            JavaApiFields.TimeInForce.value: TimeInForces.ATC.value,
            JavaApiFields.OrdType.value: OrdTypes.Market.value},
            ord_reply_block, "Check error after DirectMOC with qty=0")
        # endregion
