import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderMultiLegOMS import NewOrderMultiLegOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9051(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_4")
        self.ocr = FixMessageOrderCancelRequestOMS()
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.price = self.nos.get_parameter("Price")
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = NewOrderMultiLegOMS(self.data_set)
        self.order_submit2 = NewOrderMultiLegOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(self.environment.get_list_fe_environment()[0].user_1,
                                                 self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"InstrID": self.data_set.get_instrument_id_by_name("instrument_5")},
                                             ord_notify, "Check step 1")
        ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion
        # region Step 2
        self.order_submit2.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                  self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  SubmitRequestConst.USER_ROLE_1.value, ord_id)
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"InstrID": self.data_set.get_instrument_id_by_name("instrument_5")},
                                             ord_notify, "Check step 2")
        # endregion
