import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.es_messages.OrdReport import OrdReport
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7010(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_manager_buy = FixManager(self.fix_env.buy_side, self.test_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_market()
        self.exec = FixMessageExecutionReportOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client = self.data_set.get_client_by_name('client_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_rep = OrdReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        ord_id = response[0].get_parameter("OrderID")
        # endregion
        # region Step 2
        self.exec.set_outgoing_trade(self.nos, ord_id)
        self.fix_manager_buy.send_message_fix_standard(self.exec)
        # endregion
        # region Step 3
        self.ord_rep.set_default_open(ord_id, ord_id)
        self.ord_rep.update_fields_in_component("OrdReportBlock",
                                                {"CumQty": "50", "LeavesQty": "50", "ExecType": "Restated"})
        self.java_api_manager.send_message_and_receive_response(self.ord_rep)
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        exp_result = {"OrdType": "LMT", "ExecType": "RES", "TransStatus": "OPN", "TransExecStatus": "PFL"}
        self.java_api_manager.compare_values(exp_result, ord_rep, "Check that  order was restated")
        # endregion
