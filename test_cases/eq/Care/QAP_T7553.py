import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7553(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.nos.set_default_care_limit()
        self.java_api_manager.send_message_and_receive_response(self.nos)
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({"WashBookAccountID": self.wash_book}, ord_rep, "Check wasbook")
        # endregion
