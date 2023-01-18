import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T6885(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.cancel_request = CancelOrderRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_message.set_default_care_limit("instrument_1")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion
        # region Step 2-3
        qty = int(self.fix_message.get_parameter('OrderQtyData')['OrderQty']) / 2
        price = self.fix_message.get_parameter('Price')
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client,
                                                                                            self.mic, float(price),
                                                                                            int(qty), delay=1)
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            child_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id) \
                .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region Step 4
        self.ssh_client.send_command("~/quod/script/site_scripts/db_endOfDay_postgres")
        # endregion
        # region Step 5
        try:
            trade_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.fix_env.buy_side, self.venue_client,
                                                                              self.mic, True)
            self.cancel_request.set_default(order_id, "Y", "Y")
            self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value}
        self.java_api_manager.compare_values(expected_result, ord_notify, "Check TransStatus")
        ord_notify_child = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, child_ord_id).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value}
        self.java_api_manager.compare_values(expected_result, ord_notify_child, "Check TransStatus for child")
        # endregion
