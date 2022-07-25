import logging
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
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_6375(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.alloc_account = 'test'
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order via FIX
        no_allocs: dict = {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'PreAllocGrp': no_allocs})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion

        # region Check Alt Account in Pre Trade Allocations tab
        alt_account_id = self.order_book.extract_2lvl_fields(tab='Pre Trade Allocations', column_names=['Id'], rows=[1],
                                                             filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id})
        self.order_book.compare_values({'Id': self.alloc_account}, alt_account_id[0],
                                       'Check Id in Pre Trade Allocations tab')
        # endregion

        # region Execute CO
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region Complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Book order and checking values after it in the Order book
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        self.middle_office.allocate_block()
        # endregion

        # region Checking Alt Account in Allocations
        alt_account = self.middle_office.extract_allocate_value(column_name=AllocationsColumns.alt_account.value)
        self.middle_office.compare_values({AllocationsColumns.alt_account.value: self.alloc_account}, alt_account,
                                          'Checking Alt Account in Allocations')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
