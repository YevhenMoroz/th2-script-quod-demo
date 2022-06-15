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
        first_all_details = self.order_book.extract_2lvl_fields(SecondLevelTabs.pre_trade_alloc_tab.value,
                                                                [PreTradeAllocations.id.value,
                                                                 PreTradeAllocations.qty.value], [1],
                                                                {OrderBookColumns.order_id.value: order_id})
        self.order_book.compare_values({"Id": self.client_all_2, "Quantity": "50"},
                                       {"Id": first_all_details[0]["Id"], "Quantity":first_all_details[0]["Quantity"]},
                                       "Check Trade Allocation")
        second_all_details = self.order_book.extract_2lvl_fields(SecondLevelTabs.pre_trade_alloc_tab.value,
                                                                 [PreTradeAllocations.id.value,
                                                                  PreTradeAllocations.qty.value], [2],
                                                                 {OrderBookColumns.order_id.value: order_id})
        self.order_book.compare_values({"Id": self.client_all_1, "Quantity": "50"},
                                       {"Id":second_all_details[0]["Id"], "Quantity": second_all_details[0]["Quantity"]},
                                       "Check Trade Allocation")
        # endregion
        # region split order
        self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id])
        child_id = self.order_book.extract_2lvl_fields(
            SecondLevelTabs.child_tab.value, [ChildOrderBookColumns.order_id.value], [1], {OrderBookColumns.order_id.value: order_id})
        # endregion
        # region get details from child order
        first_child_all_id = self.child_book.get_child_order_sub_lvl_value(1,
                                                                               ChildOrderBookColumns.id_allocation.value,
                                                                               ChildOrderBookColumns.pre_all_tab.value,
                                                                               {ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        sec_child_all_id = self.child_book.get_child_order_sub_lvl_value(2,
                                                                            ChildOrderBookColumns.id_allocation.value,
                                                                            ChildOrderBookColumns.pre_all_tab.value,
                                                                            {
                                                                                ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        first_child_all_qty = self.child_book.get_child_order_sub_lvl_value(1,
                                                                            ChildOrderBookColumns.qty_alloc.value,
                                                                            ChildOrderBookColumns.pre_all_tab.value,
                                                                            {
                                                                                ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        sec_child_all_qty = self.child_book.get_child_order_sub_lvl_value(2,
                                                                            ChildOrderBookColumns.qty_alloc.value,
                                                                            ChildOrderBookColumns.pre_all_tab.value,
                                                                            {
                                                                                ChildOrderBookColumns.order_id.value: child_id[0]['ID']})
        # endregion
        # region check alloc in child order
        self.child_book.compare_values({"ID": self.client_all_2, "Qty": "50"}, {"ID": first_child_all_id, "Qty": first_child_all_qty},
                                       "Check first allocation details")
        self.child_book.compare_values({"ID": self.client_all_1, "Qty": "50"},
                                       {"ID": sec_child_all_id, "Qty": sec_child_all_qty},
                                       "Check second allocation details")
        # endregion
