import time
from rule_management import RuleManager, Simulators
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.CheckInOrderRequest import CheckInOrderRequest
from test_framework.java_api_wrappers.ors_messages.CheckOutOrderRequest import CheckOutOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7524(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client_venue = self.data_set.get_venue_client_names_by_name(
            "client_pt_1_venue_1")
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.new_qty = "4444"
        self.cancel_replace_report = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.check_out = CheckOutOrderRequest()
        self.check_in = CheckInOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region check out order
        self.check_out.set_default(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.check_out)
        self.return_result(responses, ORSMessageType.OrdNotification.value)
        notify_block = self.result.get_parameter('OrdNotificationBlock')
        self.java_api_manager.compare_values({JavaApiFields.IsLocked.value: OrderReplyConst.IsLocked_Y.value},
                                             notify_block, "Check order values after check out")
        # endregion

        # region amend order via FIX
        cancel_replace_rule = None
        try:
            cancel_replace_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                                              self.client_venue,
                                                                                              self.venue)
            cancel_replace_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(
                self.fix_message)
            cancel_replace_request.change_parameter('OrderQtyData', {'OrderQty': self.new_qty})
            self.fix_manager.send_message_and_receive_response_fix_standard(cancel_replace_request)
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            self.rule_manager.remove_rule(cancel_replace_rule)

        self.cancel_replace_report.set_default(self.fix_message)
        self.cancel_replace_report.change_parameter("Text", "11629 Order is in locked state")
        self.fix_verifier.check_fix_message_fix_standard(self.cancel_replace_report)
        # endregion

        # region check in order
        self.check_in.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.check_in)
        # endregion

        # region amend order via FIX
        try:
            cancel_replace_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                                              self.client_venue,
                                                                                              self.venue)
            cancel_replace_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(
                self.fix_message).change_parameter('OrderQtyData', {'OrderQty': self.new_qty})
            self.fix_manager.send_message_fix_standard(cancel_replace_request)
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            self.rule_manager.remove_rule(cancel_replace_rule)
        # endregion
        self.cancel_replace_report.set_default(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.cancel_replace_report)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response