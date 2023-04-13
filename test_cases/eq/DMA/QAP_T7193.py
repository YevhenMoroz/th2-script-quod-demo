import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7193(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.ord_can = FixMessageOrderCancelRequestOMS()
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        price = self.fix_message.get_parameter("Price")
        qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        rule = None
        # endregion

        # region Step 1-2
        try:
            rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.fix_env.buy_side, client_for_rule, exec_destination, float(price), int(qty), 0)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(rule)
        exec_rep = self.fix_manager.get_first_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "2", 'ExecType': 'F'}, exec_rep, "Check Order")
        # endregion
        # region Step 3
        self.ord_can.set_default(self.fix_message)
        try:
            rule = self.rule_manager.add_OrderCancelRequest(
                self.fix_env.buy_side, client_for_rule, exec_destination, True)
            self.fix_manager.send_message_and_receive_response(self.ord_can)
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(rule)
        can_rej = self.fix_manager.get_last_message("OrderCancelReject").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "2", 'CxlRejReason': '0', "ClOrdID": cl_ord_id}, can_rej,
                                        "Check CancelReject")
        # endregion
