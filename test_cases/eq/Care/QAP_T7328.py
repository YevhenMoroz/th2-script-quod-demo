import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7328(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = FixNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.new_washbook = self.data_set.get_washbook_account_by_name('washbook_account_3')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        self.java_api_manager.send_message_and_receive_response(self.nos)
        ord_not = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            "OrdNotificationBlock"]
        exp_res = {"WashBookAccountID": self.new_washbook}
        self.java_api_manager.compare_values(exp_res, ord_not, "Check Client and Sts")
        # endregion
