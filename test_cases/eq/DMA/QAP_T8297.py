import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, TimeInForces, OrdTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8297(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create LimitOnClose DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {'CustOrderHandlingInst': "LOC",
                                                      JavaApiFields.TimeInForce.value: TimeInForces.DAY.value,
                                                      })
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 1: check result
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value). \
            get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
             JavaApiFields.OrdType.value: OrdTypes.Limit.value,
             JavaApiFields.CustOrderHandlingInst.value: OrderReplyConst.CustOrderHandlingInst_LOC.value}, ord_notif,
            'Check order values')
        # endregion
