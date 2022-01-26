import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_5483(TestCase):
    def __init__(self, report_id, session_id, data_set):
        super().__init__(report_id, session_id, data_set)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        fix_manager = FixManager(ss_connectivity)
        qty = '5000'
        fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        fix_message.set_default_care_limit()
        fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_8'))
        print(fix_message.get_parameters())
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        price = fix_message.get_parameter('Price')
        order_id_column = OrderBookColumns.order_id.value
        client_id_column = OrderBookColumns.client_id.value
        # endregion
        order_id_first = None
        order_id_second = None
        # region create 2 DMA order
        fix_manager.send_message_fix_standard(fix_message)
        order_id_first = order_book.extract_field(OrderBookColumns.order_id.value)
        client_inbox.accept_order(qty, qty, qty)
        fix_manager.send_message_fix_standard(fix_message)
        order_id_second = order_book.extract_field(OrderBookColumns.order_id.value)
        client_inbox.accept_order(qty, qty, qty)

        # endregion
        print(order_id_first)
        print(order_id_second)
        # region mass modify
        ord_ticket = OMSOrderTicket(self.case_id, self.session_id)
        ord_ticket.set_order_details(self.data_set.get_client_by_name('client_pt_1'), "20", qty="100")
        ord_ticket.mass_modify_order(2)
        # endregion

        # region compare values
        order_book.set_filter([order_id_column, order_id_first])
        client_id1 = order_book.extract_field(client_id_column)
        order_book.set_filter([order_id_column, order_id_second])
        client_id2 = order_book.extract_field(client_id_column)
        order_book.compare_values({'OrderID_1': self.data_set.get_client_by_name('client_pt_1'),
                                   'OrderID_2': self.data_set.get_client_by_name('client_pt_1')},
                                  {'OrderID_1': client_id1, 'OrderID_2': client_id2}, 'Comparing values')
        # endregion
