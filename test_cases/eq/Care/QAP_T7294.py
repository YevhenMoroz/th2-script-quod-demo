import logging
import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7294(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        # endregion

        # region split first order
        self.__split_order(order_id, cl_ord_id, str(int(self.qty) + 1))
        # endregion

        # region check values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameter(
            JavaApiFields.NewOrderReplyBlock.value)['Ord']
        child_ord_id = ord_reply_block['OrdID']
        self.java_api_manager.compare_values({
            JavaApiFields.FreeNotes.value: f'11801 Validation by CS failed, Request not allowed:  Quantity of child order is higher than the UnmatchedQty of care order, OrdID={child_ord_id}'},
            ord_reply_block, "Check error when split qty > parent qty")
        # endregion

        # region second split order
        self.__split_order(order_id, cl_ord_id, self.qty)
        # endregion

        # region check values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({
            JavaApiFields.OrdQty.value: self.qty + '.0',
            JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            ord_reply_block, "Check child order after slitting on full qty")
        # endregion

        # region second split order
        self.__split_order(order_id, cl_ord_id, self.qty)
        # endregion

        # region check values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameter(
            JavaApiFields.NewOrderReplyBlock.value)['Ord']
        child_ord_id = ord_reply_block['OrdID']
        self.java_api_manager.compare_values({
            JavaApiFields.FreeNotes.value: f'11801 Validation by CS failed, Request not allowed:  Quantity of child order is higher than the UnmatchedQty of care order, OrdID={child_ord_id}'},
            ord_reply_block, "Check error after splitting order without leaves qty")
        # endregion

    def __split_order(self, order_id, cl_ord_id, qty):
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            self.order_submit.set_default_child_dma(order_id, cl_ord_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                         {'ListingList': {'ListingBlock': [
                                                             {
                                                                 'ListingID': self.data_set.get_listing_id_by_name(
                                                                     "listing_3")}]},
                                                             'InstrID': self.data_set.get_instrument_id_by_name(
                                                                 "instrument_2"),
                                                             'Price': self.price,
                                                             'OrdQty': qty,
                                                             "ClOrdID": basic_custom_actions.client_orderid(9)
                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
