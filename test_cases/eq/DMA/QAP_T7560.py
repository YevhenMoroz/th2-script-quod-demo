import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7560(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')  # 36ONE_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order
        responses = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            # Creating 30 executions
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check
        self.__return_result(responses, ORSMessageType.OrderReply.value)
        order_reply_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values({JavaApiFields.OrdCapacity.value: OrderReplyConst.OrdCapacity_A.value,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply_block, 'Check Order Capacity')
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
