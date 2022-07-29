import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, \
    PreTradeAllocations, SecondLevelTabs, ChildOrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_4433(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.price = '35'
        self.qty = '100'
        self.desk = environment.get_list_fe_environment()[0].desk_2
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.client_all_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.client_all_2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        self.child_book = OMSChildOrderBook(self.test_id, self.session_id)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        alloc_det = {self.client_all_1: "50", self.client_all_2: '50'}
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            tif=TimeInForce.DAY.value, recipient=self.desk,
                                            partial_desk=False, alloc_details=alloc_det)
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # check 2lvl fields
        self.__check_alloc_details(PreTradeAllocations.id.value, self.client_all_1, 1, [OrderBookColumns.order_id.value, order_id])
        self.__check_alloc_details(PreTradeAllocations.qty.value, "50", 1, [OrderBookColumns.order_id.value, order_id])
        self.__check_alloc_details(PreTradeAllocations.id.value, self.client_all_2, 2, [OrderBookColumns.order_id.value, order_id])
        self.__check_alloc_details(PreTradeAllocations.qty.value, "50", 2, [OrderBookColumns.order_id.value, order_id])
        # endregion
        # region split order
        self.order_ticket.set_order_details(qty=self.qty)
        self.order_ticket.split_order()
        child_id = self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).extract_2lvl_fields(
            SecondLevelTabs.child_tab.value, [ChildOrderBookColumns.order_id.value], [1])
        # endregion
        # region get details from child order
        self.__check_alloc_details_of_child(ChildOrderBookColumns.id_allocation.value, self.client_all_1, {ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        self.__check_alloc_details_of_child(ChildOrderBookColumns.qty_alloc.value, "50",
                                            {ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        self.__check_alloc_details_of_child(ChildOrderBookColumns.id_allocation.value, self.client_all_2,
                                            {ChildOrderBookColumns.order_id.value: child_id[0]['ID']}, 2)
        self.__check_alloc_details_of_child(ChildOrderBookColumns.qty_alloc.value, "50",
                                            {ChildOrderBookColumns.order_id.value: child_id[0]['ID']}, 2)
        # endregion

    def __check_alloc_details(self, field:str, expected_res:str, numb_row:int = 1, filter:list=None):
        all_details = self.order_book.set_filter(filter).extract_2lvl_fields(SecondLevelTabs.pre_trade_alloc_tab.value,
                                                               [field], [numb_row])
        self.order_book.compare_values({field: expected_res},
                                       {field: all_details[0][field]},
                                       "Check Trade Allocation")



    def __check_alloc_details_of_child(self, field:str, expected_res:str, filter:dict=None, row:int = 1):
        all_details =  self.child_book.get_child_order_sub_lvl_value(row,field,
                                                                               ChildOrderBookColumns.pre_all_tab.value,
                                                                               filter)
        self.order_book.compare_values({field: expected_res},
                                       {field: all_details},
                                       "Check Trade Allocation")