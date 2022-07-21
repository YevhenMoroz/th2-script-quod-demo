import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ChildOrderBookColumns, \
    SecondLevelTabs, ExecSts, DoneForDays
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4536(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.child_book = OMSChildOrderBook(self.test_id, self.session_id)
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region do split order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            self.order_ticket.split_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        dma_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                     [ChildOrderBookColumns.order_id.value], [1])
        # endregion
        # region cancel dma order
        self.child_book.cancel_order(filter_list=[ChildOrderBookColumns.order_id.value, dma_id[0]['ID']])
        self.order_book.check_second_lvl_fields_list({OrderBookColumns.sts.value: ExecSts.cancelled.value})
        # endregion
        # region manual exec
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: order_id})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.done_for_day.value: DoneForDays.yes.value})
        # endregion
