import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_5684(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '1000'
        self.price = '1234'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_2')  # MOClient_EUREX
        self.venue = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message_first = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_second = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            # first order
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message_first.set_default_dma_limit(instr='instrument_3')
            self.fix_message_first.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            response_first = self.fix_manager.send_message_and_receive_response(self.fix_message_first)
            # get Client Order ID and Order ID
            cl_ord_id_first = response_first[0].get_parameters()['ClOrdID']
            order_id_first = response_first[0].get_parameters()['OrderID']

            # second order
            self.fix_message_second.set_default_dma_limit(instr='instrument_3')
            self.fix_message_second.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            response_second = self.fix_manager.send_message_and_receive_response(self.fix_message_second)
            # get Client Order ID and Order ID
            cl_ord_id_second = response_second[0].get_parameters()['ClOrdID']
            order_id_second = response_second[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Mass Book orders and checking PostTradeStatus in the Order book
        self.order_book.mass_book([1, 2])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_first])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Mass Book of the first order')
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_second])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Mass Book of the second order')
        # endregion

        # region Checking the values after the Mass Book in the Middle Office
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.qty.value, MiddleOfficeColumns.price.value],
            [MiddleOfficeColumns.order_id.value, order_id_first])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.qty.value: '1,000', MiddleOfficeColumns.price.value: '12.34'}, values_after_book,
            'Comparing Qty and Price in the MiddleOffice after the Book of the first block')

        values_after_book2 = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.qty.value, MiddleOfficeColumns.price.value],
            [MiddleOfficeColumns.order_id.value, order_id_second])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.qty.value: '1,000', MiddleOfficeColumns.price.value: '12.34'}, values_after_book2,
            'Comparing Qty and Price in the MiddleOffice after the Book of the second block')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
