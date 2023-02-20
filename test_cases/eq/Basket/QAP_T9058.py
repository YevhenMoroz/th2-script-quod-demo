import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BasketMessagesConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9058(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.remove_order_from_basket_request = RemoveOrdersFromOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        # endregion

        # region get order_id
        list_id = list_notify_block['OrderListID']
        ord_id1 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        ord_id2 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][1]['OrdID']
        list_of_orders = [ord_id1, ord_id2]
        # endregion

        # region remove first order from basket
        order_ids_list = []
        for order in list_of_orders:
            dict = {"OrdID": order}
            order_ids_list.append(dict)
        self.remove_order_from_basket_request.set_default(ord_id1, list_id)
        self.remove_order_from_basket_request.update_fields_in_component('RemoveOrdersFromOrderListRequestBlock',
                                                                         {"OrdIDList": {"OrdIDBlock": order_ids_list}})
        self.java_api_manager.send_message_and_receive_response(self.remove_order_from_basket_request)
        self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        # endregion

        # region check values
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_DON.value}, list_notify_block,
            'Check basket status after orders removing')
        # endregion
