import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7633(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.price = '20'
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.order_cancel_request = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region split limit order
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names, self.venue,
                int(self.price))
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'Price': self.price,
                                                                                 'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                     "instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check UnmatchedQty of the parent order
        ord_update_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdUpdate.value).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: '0.0'},
                                             ord_update_block,
                                             'Check UnmatchedQty of parent order after Split Limit action')
        ord_notofy_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        child_order_id = ord_notofy_block['OrdID']
        # endregion

        # region cancel child order
        cancel_rule = None
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names, self.venue, True)
            self.order_cancel_request.set_default(child_order_id)
            self.java_api_manager.send_message_and_receive_response(self.order_cancel_request)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region check UnmatchedQty after cancellation
        ord_update_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdUpdate.value).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: '100.0'},
                                             ord_update_block,
                                             'Check UnmatchedQty of parent order after child order cancellation')
        # endregion

        # region check UnmatchedQty after cancellation
        ord_reply_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value},
                                             ord_reply_block,
                                             'Check Child Order Sts')
        # endregion