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


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6913(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '7984'
        price = '10'
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameters({'Account': self.data_set.get_client_by_name('client_pt_1'),
                                            'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'),
                                            'Price': price, 'OrderQtyData': {'OrderQty': qty},
                                            'ExDestination': self.exec_destination})
        new_order_single_rule = trade_rule = None
        # endregion
        # region send fix message and trade it (step 1, step 2, step 3)
        try:
            # self.rule_manager.add
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                self.exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_ExecutionReportTradeByOrdQtyWithLastLiquidityInd_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                self.exec_destination,
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

        # region check 35=8, 39=0 message(step 2)
        ignored_list = ['Parties', 'ReplyReceivedTime', 'SecondaryOrderID', 'LastMkt', 'Text']
        self.fix_execution_report.set_default_new(self.fix_message)
        # self.fix_execution_report.add_tag({'LastLiquidityInd': '1'})
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_report, ignored_fields=ignored_list)
        # endregion

        # region check 35=8, 39=2 message(step 3)
        ignored_list = ['ReplyReceivedTime', 'Account', 'SettlCurrency', 'LastMkt', 'Text', 'SecurityDesc']
        self.fix_execution_report.set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_report, ignored_fields=ignored_list)
        # endregion

        # region check 35=8, 39=2 message(step 4)
        ignored_list = ['Parties', 'QuodTradeQualifier', 'BookID', 'SettlCurrency', 'TradeReportingIndicator',
                        'NoParty', 'tag5120', 'LastMkt', 'Text', 'ExecBroker', 'SecurityDesc']
        self.fix_execution_report.set_default_filled(self.fix_message)
        self.fix_execution_report.add_tag({'LastLiquidityInd': '1'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.fix_execution_report, ignored_fields=ignored_list)
        # endregion
