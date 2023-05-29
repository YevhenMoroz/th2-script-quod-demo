import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7337(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[
            0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_message = FixNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.account = self.data_set.get_account_by_name('client_co_1_dummy_acc')
        self.instrument = self.data_set.get_java_api_instrument('instrument_3')
        self.qty = '100'
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order (Preconditions)
        self.fix_message.set_default_care_limit()
        self.fix_message.update_fields_in_component('NewOrderSingleBlock',
                                                    {'ClientAccountGroupID': self.client, "PreTradeAllocationBlock": {
                                                        "PreTradeAllocationList": {
                                                            "PreTradeAllocAccountBlock":
                                                                [{
                                                                    "AllocClientAccountID": self.account,
                                                                    "AllocQty": self.qty}]}},
                                                     'InstrumentBlock': self.instrument, 'OrdQty': self.qty})
        self.java_api_manager.send_message_and_receive_response(self.fix_message)
        # endregion

        # region check fields (step 1)
        ord_notif_block = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value,
                                              JavaApiFields.SingleAllocClientAccountID.value: self.account},
                                             ord_notif_block, 'Check Order status and SingleAllocClientAccountID')

        # endregion
