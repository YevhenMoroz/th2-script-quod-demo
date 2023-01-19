import logging
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7044(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.new_qty = "50"
        self.new_price = "15"
        self.venue_client_name = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.new_order_single.get_parameter('Price')
        self.test_id = create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_submit = OrderSubmitOMS(data_set)
        self.modify_request = OrderModificationRequest()
        self.nos_rule = None
        self.cancel_replace_rule = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        # endregion

        # region do split order
        self.__split_order(order_id, cl_ord_id)
        # endregion

        # check splitting values
        ord_update_block = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.UnmatchedQty.value: "0.0", JavaApiFields.LeavesQty.value: self.qty + ".0"},
            ord_update_block, 'Check values of parent order after splitting')
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecStatus_OPN.value,
                                              JavaApiFields.OrdQty.value: self.qty + '.0',
                                              JavaApiFields.Price.value: self.price + self.price},
                                             ord_reply_block, 'Check values of child order after splitting')
        # endregion

        # region send cancel replace request
        self.__send_cancel_replace_request(order_id)
        # endregion

        # region check values after amending
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.UnmatchedQty.value: "0.0", JavaApiFields.LeavesQty.value: self.new_qty + ".0",
             JavaApiFields.OrdQty.value: self.new_qty + ".0", JavaApiFields.Price.value: self.new_price + ".0"},
            ord_reply_block, 'Check values of parent order after modification')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        if self.nos_rule:
            self.rule_manager.remove_rule(self.nos_rule)
        if self.cancel_replace_rule:
            self.rule_manager.remove_rule(self.cancel_replace_rule)

    def __split_order(self, order_id, cl_ord_id):
        self.nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
            self.fix_env.buy_side, self.venue_client_name,
            self.mic, float(self.price))
        self.order_submit.set_default_child_dma(order_id, cl_ord_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_3")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)

    def __send_cancel_replace_request(self, order_id):
        self.cancel_replace_rule \
            = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                          self.venue_client_name,
                                                                          self.mic)
        self.modify_request.set_default(self.data_set, order_id)
        self.modify_request.update_fields_in_component('OrderModificationRequestBlock',
                                                       {'OrdQty': self.new_qty, 'Price': self.new_price})
        self.java_api_manager.send_message_and_receive_response(self.modify_request)
