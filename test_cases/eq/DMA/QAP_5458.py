import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns, TradeBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_5458(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.trade_book = OMSTradesBook(self.case_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        qty = '5448'
        price = '10'
        lookup = self.data_set.get_lookup_by_name('lookup_2')
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_client_by_name('client_pt_1')
        tif = 'Day'
        display_qty = str(int(int(qty) / 2))
        filter_list_order_book = [OrderBookColumns.qty.value, qty]
        self.order_ticket.set_order_details(client, price, qty=qty, tif=tif, display_qty=display_qty)
        new_order_single_rule = trade_rule = None

        # region step 1 and step 2
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            exec_destination,
                                                                                            float(price),
                                                                                            int(display_qty), delay=0)
            self.order_ticket.create_order(lookup)
        except Exception as e:
            logger.info(f'Exception of your execution is {e}')

        finally:
            self.rule_manager.remove_rule(new_order_single_rule)
            self.rule_manager.remove_rule(trade_rule)

        # endregion

        # region extract execution and check value in trade blotter
        self.order_book.set_filter(filter_list_order_book)
        execution = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                        [TradeBookColumns.exec_id.value],
                                                        [1])
        new_display_qty = display_qty[0] + ',' + display_qty[1] + display_qty[2:4]
        self.trade_book.set_filter([TradeBookColumns.exec_id.value, execution[0]['ExecID']])
        unmatched_qty = self.trade_book.extract_field(TradeBookColumns.unmatched_qty.value)
        self.trade_book.compare_values({TradeBookColumns.unmatched_qty.value: new_display_qty},
                                       {TradeBookColumns.unmatched_qty.value: unmatched_qty},
                                       'Comparing of UnmatchedQty')
        # endregion
