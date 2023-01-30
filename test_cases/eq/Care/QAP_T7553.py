import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7553(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_3')
        self.account = self.data_set.get_account_by_name('client_1_acc_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'PreTradeAllocationBlock': {'PreTradeAllocationList': {
                                                         "PreTradeAllocAccountBlock": [
                                                             {'AllocAccountID': self.account, 'AllocQty': '100'}]}},
                                                         'WashBookAccountID': self.wash_book})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_not = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            "OrdNotificationBlock"]
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book,
                                              JavaApiFields.SingleAllocAccountID.value: self.account}, ord_not,
                                             "Check washbook and account")
        # endregion
