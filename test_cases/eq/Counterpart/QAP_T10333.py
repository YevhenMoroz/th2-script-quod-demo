import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10333(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name('client_counterpart_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.manual_execute = TradeEntryOMS(self.data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.order_modification_request = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order:
        recipient = self.environment.get_list_fe_environment()[0].user_1
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        role = SubmitRequestConst.USER_ROLE_1.value
        self.order_submit.set_default_care_limit(recipient=recipient,
                                                 desk=desk,
                                                 role=role)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.AccountGroupID.value: self.client
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, f'Verify that order {order_id} has Sts = Open (step 1)')
        reg_body = self.data_set.get_counterpart_id_java_api('counterpart_regulatory_body_venue')
        invest_firm = self.data_set.get_counterpart_id_java_api('counterpart_investor_firm_cl_counterpart')
        market_maker_th2_route = self.data_set.get_counterpart_id_java_api('counterpart_market_maker_th2_route')
        custodian_user = self.data_set.get_counterpart_id_java_api('counterpart_custodian_user')
        custodian_user_2 = self.data_set.get_counterpart_id_java_api('counterpart_custodian_user_2')
        contra_firm = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        counterpart_list_for_checking = [invest_firm, reg_body, market_maker_th2_route, custodian_user]
        actually_list_of_counterpart = order_reply[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        self.check_that_counterparts_are_present(counterpart_list_for_checking, actually_list_of_counterpart, 'step 1')
        # endregion

        # region step 2-4: Modify Counterparts for order:

        conterpart_modification_list = [reg_body, invest_firm, market_maker_th2_route, contra_firm, custodian_user_2]
        self.order_modification_request.set_default_amend_counterparts(order_id, conterpart_modification_list)
        self.java_api_manager.send_message_and_receive_response(self.order_modification_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        actually_list_of_counterpart = order_reply[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        self.check_that_counterparts_are_present(conterpart_modification_list, actually_list_of_counterpart, 'step 4')
        # endregion

    def check_that_counterparts_are_present(self, counterpart_list_for_checking, actually_list_of_counterpart, step):
        counterpart_check = False
        for counterpart in counterpart_list_for_checking:
            for actually_counterpart in actually_list_of_counterpart:
                if counterpart['PartyRole'] in actually_counterpart.values() and counterpart[
                    'CounterpartID'] in actually_counterpart.values():
                    counterpart_check = True
                    break
                else:
                    counterpart_check = False
            if counterpart_check:
                self.java_api_manager.compare_values({'CounterpartPresent': 'True'},
                                                     {'CounterpartPresent': str(counterpart_check)},
                                                     f'Verify that {counterpart} is present ({step})')
