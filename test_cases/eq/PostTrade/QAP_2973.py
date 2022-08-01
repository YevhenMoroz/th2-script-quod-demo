import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExchangeRateCalc, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_2973(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.all_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.currency = self.data_set.get_currency_by_name('currency_5')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('Account', self.client)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            # endregion
            # region create order
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            time.sleep(10)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(nos_rule)
        #  endregion
        # region book order
        self.mid_office.set_modify_ticket_details(toggle_recompute=True, settl_currency=self.currency,
                                                  exchange_rate='2', exchange_rate_calc=ExchangeRateCalc.multiple.value)
        self.mid_office.book_order([OrderBookColumns.order_id.value, order_id])
        #  endregion
        # region check Alloc Report
        self.allocation_message.set_default_ready_to_book(self.fix_message)
        self.allocation_message.change_parameters(
            {'AvgPx': str(int(self.price) * 2), 'Currency': self.currency, 'RootSettlCurrency': self.currency,
             "RootSettlCurrAmt": str(int(self.price) * 2 * int(self.qty)),
             'tag5120': "*", "GrossTradeAmt": str(int(self.price) * 2 * int(self.qty)),
             'NetMoney': str(int(self.price) * 2 * int(self.qty))})
        self.fix_verifier.check_fix_message_fix_standard(self.allocation_message)
        #  endregion
        # region approve and allocate
        self.mid_office.approve_block()
        param = [{"Security Account": self.all_acc, "Alloc Qty": self.qty}]
        self.mid_office.set_modify_ticket_details(is_alloc_amend=True, arr_allocation_param=param)
        self.mid_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id])
        #  endregion
        # region check confirmation report
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters(
            {'AvgPx': str(int(self.price) * 2), 'Currency': self.currency, "tag5120": "*",
             "GrossTradeAmt": str(int(self.price) * 2 * int(self.qty)),
             "NetMoney": str(int(self.price) * 2 * int(self.qty)),
             "SettlCurrAmt": str(int(self.price) * 2 * int(self.qty) * 2), "SettlCurrency": self.currency,
              "Account": self.client, "AllocInstructionMiscBlock2": '*', "AllocNetPrice": str(int(self.price) * 2)})
        self.fix_verifier.check_fix_message_fix_standard(conf_report)
        #  endregion
