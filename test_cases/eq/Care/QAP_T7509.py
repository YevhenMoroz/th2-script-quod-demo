import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7509(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.new_client = self.data_set.get_client("client_2")
        self.order_submit = OrderSubmitOMS(data_set)
        self.order_modify = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO order

        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)

        old_client = self.order_submit.get_parameters()['NewOrderSingleBlock']['AccountGroupID']
        qty = str(float(self.order_submit.get_parameters()['NewOrderSingleBlock']['OrdQty']))

        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AccountGroupID.value: old_client,
             JavaApiFields.AccountGroupName.value: old_client,
             JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
             JavaApiFields.LeavesQty.value: qty,
             JavaApiFields.UnmatchedQty.value: qty},
            order_reply,
            f'Checking expected and actually results for {order_id} (step 1)')
        # endregion

        # region step 2 and step 3: Modify client for CO orders
        self.order_modify.set_default(self.data_set, order_id)
        self.order_modify.update_fields_in_component('OrderModificationRequestBlock',
                                                     {'AccountGroupID': self.new_client})
        self.java_api_manager.send_message_and_receive_response(self.order_modify)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AccountGroupID.value: self.new_client,
                                              JavaApiFields.AccountGroupName.value: self.new_client}, order_reply,
                                             f'Checking that order {order_id} changed client (step 3)')
        # endregion
