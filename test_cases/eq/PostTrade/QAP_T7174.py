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


class QAP_T7174(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.client2 = self.data_set.get_client('client_pt_2')  # MOClient2
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Book order and checking PostTradeStatus in the Order book
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Checking the ClientID
        client_id = self.middle_office.extract_block_field(MiddleOfficeColumns.client_id.value,
                                                           [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values({MiddleOfficeColumns.client_id.value: self.client}, client_id,
                                          'Comparing ClientID after Book in the Middle Office')
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [
            {'Security Account': self.data_set.get_account_by_name('client_pt_1_acc_1'), 'Alloc Qty': self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Unallocate block and Unbook order
        self.middle_office.unallocate_order([MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.un_book_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region re-Book order
        self.middle_office.set_modify_ticket_details(client=self.client2)
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Changing the Client and checking the new ClientID
        client_id2 = self.middle_office.extract_block_field(MiddleOfficeColumns.client_id.value,
                                                            [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values({MiddleOfficeColumns.client_id.value: self.client2}, client_id2,
                                          'Comparing new ClientID after re-Book in the Middle Office')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
