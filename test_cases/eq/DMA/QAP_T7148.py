import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7148(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_1")
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        self.cancel_request = FixMessageOrderCancelRequestOMS()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region  step 1: create DMA order via FIX
        self.new_order.set_default_care_limit(account='client_1')
        self.new_order.add_tag({'header': {
            JavaApiFields.SenderSubID.value: 'SENDER_SUB_ID',
            JavaApiFields.TargetSubID.value: 'TARGET_SUB_ID',
            JavaApiFields.DeliverToCompID.value: 'DELIVER_TO_COMP_ID',
            JavaApiFields.DeliverToSubID.value: 'DELIVER_TO_SUB_ID',
            JavaApiFields.OnBehalfOfCompID.value: 'ON_BEHALF_OF_COMP_ID',
            JavaApiFields.OnBehalfOfSubID.value: 'ON_BEHALF_OF_SUB_ID'
        }})
        price = self.new_order.get_parameters()['Price']
        new_order_single = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(price))
            self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single)
        # endregion

        # region step 2:
        list_ignore_field = ['CxlRejResponseTo', 'Account',
                             'Text', 'MsgType', 'MsgSeqNum',
                             'TargetCompID', 'SenderCompID', 'BeginString',
                             'BodyLength', 'ApplVerID', 'SendingTime',
                             'SettlDate', 'TimeInForce', 'Currency',
                             'HandlInst', 'OrderCapacity', 'QtyType', 'OrigClOrdID', 'GatingRuleCondName',
                             'GatingRuleName','CxlQty']
        self.execution_report_fix.set_default_new(self.new_order)
        self.execution_report_fix.change_parameters({'header': {
            JavaApiFields.SenderSubID.value: 'TARGET_SUB_ID',
            JavaApiFields.TargetSubID.value: 'SENDER_SUB_ID',
            JavaApiFields.DeliverToCompID.value: 'ON_BEHALF_OF_COMP_ID',
            JavaApiFields.DeliverToSubID.value: 'ON_BEHALF_OF_SUB_ID',
            JavaApiFields.OnBehalfOfCompID.value: 'DELIVER_TO_COMP_ID',
            JavaApiFields.OnBehalfOfSubID.value: 'DELIVER_TO_SUB_ID',
        }, 'ExecType': '0', 'OrdStatus': '0'})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report_fix, ignored_fields=list_ignore_field,
                                                         ignore_header=False)
        # endregion

        self.cancel_request.set_default(self.new_order)
        canc_rule = None
        try:
            canc_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.fix_env.buy_side,
                                                                             self.venue_client_names,
                                                                             self.venue,
                                                                             True)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.cancel_request)
        except Exception as e:
            logger.error(f'Something gone wrong : {e}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(canc_rule)

        self.execution_report_fix.set_default_canceled(self.new_order)
        self.execution_report_fix.change_parameters({'header': {
            JavaApiFields.SenderSubID.value: 'TARGET_SUB_ID',
            JavaApiFields.TargetSubID.value: 'SENDER_SUB_ID',
            JavaApiFields.DeliverToCompID.value: 'ON_BEHALF_OF_COMP_ID',
            JavaApiFields.DeliverToSubID.value: 'ON_BEHALF_OF_SUB_ID',
            JavaApiFields.OnBehalfOfCompID.value: 'DELIVER_TO_COMP_ID',
            JavaApiFields.OnBehalfOfSubID.value: 'DELIVER_TO_SUB_ID',
        }})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report_fix, ignored_fields=list_ignore_field,
                                                         ignore_header=False)
