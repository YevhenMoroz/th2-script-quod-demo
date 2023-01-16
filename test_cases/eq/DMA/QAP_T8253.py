import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.MarkOrderRequest import MarkOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8253(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # MOClient_PARIS
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mark_ord = MarkOrderRequest()
        self.ord_modify = OrderModificationRequest()
        self.ord_cancel = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region Step 2
        self.mark_ord.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.mark_ord)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "Y"}, ord_notify, "Check Reviewed status")
        # endregion
        # region Step 3
        self.ord_modify.set_default(self.data_set, order_id)
        try:
            mod_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                   self.venue_client_name,
                                                                                   self.mic, True)
            self.java_api_manager.send_message_and_receive_response(self.ord_modify)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(mod_rule)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "N"}, ord_notify, "Check Reviewed status")
        # endregion
        # region Step 4
        self.mark_ord.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.mark_ord)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "Y"}, ord_notify, "Check Reviewed status")
        # endregion
        # region Step 5
        self.ord_cancel.set_default(order_id)
        try:
            cnl_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                            self.venue_client_name, self.mic, True)
            self.java_api_manager.send_message_and_receive_response(self.ord_cancel)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(cnl_rule)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "N"}, ord_notify, "Check Reviewed status")
        # endregion
