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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7488(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = '300'
        self.price = '10'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_8'))
        self.fix_message.change_parameter('Price', self.price)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        self.pset = self.data_set.get_pset('pset_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        global nos_rule
        order_id_first = None
        qty_of_first_block = '100'
        qty_of_second_block = '200'
        agreed_price = '10'

        # region create  DMA order
        try:
            rule_manager = RuleManager(Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.client_for_rule,
                                                                                       self.exec_destination,
                                                                                       float(self.price),
                                                                                       int(self.qty),
                                                                                       delay=0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
            order_id_first = self.order_book.extract_field(OrderBookColumns.order_id.value)

        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion

        # region split book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        split_param_1 = self.order_book.create_split_booking_parameter(qty_of_first_block, net_gross_ind="Gross",
                                                                       pset=self.pset[0],
                                                                       settlement_currency='USD',
                                                                       settlement_type='Regular',
                                                                       toggle_recompute=True
                                                                       )
        split_param_2 = self.order_book.create_split_booking_parameter(qty_of_second_block)
        self.order_book.split_book([split_param_1, split_param_2])

        # endregion

        self.middle_office.set_filter([MiddleOfficeColumns.qty.value, qty_of_first_block])
        self.middle_office.clear_filter()
        # region verifying value after book
        value_of_first_block = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.pset.value,
                                                                                MiddleOfficeColumns.pset_bic.value],
                                                                               row_number=1)

        self.middle_office.set_filter([MiddleOfficeColumns.qty.value, qty_of_second_block])
        self.middle_office.clear_filter()
        value_of_second_block = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.pset.value,
                                                                                 MiddleOfficeColumns.pset_bic.value],
                                                                                row_number=1)

        self.middle_office.compare_values({MiddleOfficeColumns.pset.value: self.pset[0],
                                           MiddleOfficeColumns.pset_bic.value: self.pset[1]
                                           }, value_of_first_block, 'Comparing with values of  first block')

        self.middle_office.compare_values({MiddleOfficeColumns.pset.value: self.pset[0],
                                           MiddleOfficeColumns.pset_bic.value: self.pset[1]
                                           }, value_of_second_block, 'Comparing with values of  second block')
        # endregion
