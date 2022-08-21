import logging
import os
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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Status, ExecSts
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6913(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '7984'
        price = '10'
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_execution_report.set_default_filled(self.fix_message)
        self.fix_execution_report.add_tag({'LastLiquidityInd': '1'})
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        filter_list = [OrderBookColumns.cl_ord_id.value, cl_ord_id]
        new_order_single_rule = trade_rule = None
        # endregion
        # region send fix message and trade it (step 1, step 2, step 3)
        try:
            # self.rule_manager.add
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_ExecutionReportTradeByOrdQtyWithLastLiquidityInd_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price), float(price), int(qty), int(qty), 0, 1
            )
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as e:
            logger.error(f'Your Exception is {e}')
        # # endregion
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(new_order_single_rule)

        # region check value
        self.order_book.set_filter(filter_list)
        fields = self.order_book.extract_fields_list({OrderBookColumns.sts.value: OrderBookColumns.sts.value,
                                                      OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value})
        self.order_book.compare_values({OrderBookColumns.sts.value: Status.terminated.value,
                                        OrderBookColumns.exec_sts.value: ExecSts.filled.value},
                                       fields,
                                       'Matching values')
        # endregion

        # region check 35=8, 39=2 message(step 4)
        self.fix_execution_report.delete_group('Parties')
        self.fix_execution_report.add_tag({'QuodTradeQualifier': '*'})
        self.fix_execution_report.add_tag({'BookID': '*'})
        self.fix_execution_report.delete_group('SettlCurrency')
        self.fix_execution_report.delete_group('TradeReportingIndicator')
        self.fix_execution_report.add_tag({'NoParty': '*'})
        self.fix_execution_report.add_tag({'tag5120': '*'})
        self.fix_execution_report.add_tag({'LastMkt': '*'})
        self.fix_execution_report.add_tag({'Text': '*'})
        self.fix_execution_report.add_tag({'ExecBroker': '*'})
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_report)
        # endregion
