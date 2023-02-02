import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6873(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_modify_message = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_cancel_reject = FixMessageOrderCancelRejectReportOMS()
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '100'
        second_qty = '400'
        price = '20'
        venue_account = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.fix_message.set_default_care_limit()
        cl_ord_id = self.fix_message.get_parameter("ClOrdID")
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_cancel_reject.set_default(self.fix_message)
        nos_rule = modification_rule = None
        # endregion

        # region create CO order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        ord_id = self.fix_manager.get_last_message("ExecutionReport").get_parameter("OrderID")
        # endregion

        # region split CO order and verify values
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  venue_account,
                                                                                                  exec_destination,
                                                                                                  float(price))
            self.order_submit.set_default_child_dma(ord_id)
            self.order_submit.update_fields_in_component("NewOrderSingleBlock", {
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            child_ord_id = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                    JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region send modify and accept it
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequestWithDelayFixStandard(
                self.fix_env.buy_side, venue_account, exec_destination, True, delay=1)
            self.fix_modify_message.set_default(self.fix_message)
            self.fix_modify_message.change_parameter('OrderQtyData', {'OrderQty': second_qty})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_modify_message)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(modification_rule)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"LeavesQty": second_qty, "CumQty": "0"}, exec_rep, "Check Qty")
        # endregion
