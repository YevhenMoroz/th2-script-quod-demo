import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7453(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "900"
        self.price = "20"
        self.last_capacity = "Agency"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.create_basket_from_existing_orders = NewOrderListFromExistingOrders()
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.modification_fake_request = OrderModificationRequest()
        self.class_name = QAP_T7453

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration

        # region create first CO order
        responses = self.ja_manager.send_message_and_receive_response(self.order_submit)
        self.class_name.print_message("Message after creation of first CO order", responses)
        cl_ord_id_first = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.ClOrdID.value]
        order_id_first = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region create second CO order
        cl_ord_id_second = bca.client_orderid(9)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.ClOrdID.value: cl_ord_id_second})
        responses = self.ja_manager.send_message_and_receive_response(self.order_submit)
        self.class_name.print_message("Message after creation of second CO order", responses)
        order_id_second = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region create basket
        self.create_basket_from_existing_orders.set_default([order_id_first, order_id_second],
                                                            self.basket_name)
        responses = self.ja_manager.send_message_and_receive_response(self.create_basket_from_existing_orders)
        self.class_name.print_message("Message after creation of basket", responses)
        # endregion

        # check basket fields
        actually_result = self.ja_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
            JavaApiFields.NewOrderListReplyBlock.value]
        expected_result = {JavaApiFields.ListExecutionPolicy.value: BasketMessagesConst.ListExecutionPolicy_C.value,
                           JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value,
                           JavaApiFields.OrderListName.value: self.basket_name}
        self.ja_manager.compare_values(expected_result, actually_result, 'Comparing value after creation of basket')
        basket_id = actually_result.get(JavaApiFields.OrderListID.value)
        # endregion

        # check order in Order Book and  Sts of orders
        self.fake_request(order_id_first, basket_id)
        self.fake_request(order_id_second, basket_id)
        # endregion

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())

    def fake_request(self, order_id, basket_id):
        self.modification_fake_request.set_default(self.data_set, order_id)
        responses = self.ja_manager.send_message_and_receive_response(self.modification_fake_request)
        self.class_name.print_message(f"Fake update for getting order`s reply({order_id})", responses)
        actually_result = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                           JavaApiFields.OrderListID.value: basket_id}
        self.ja_manager.compare_values(expected_result, actually_result, 'Compare values of orders')
