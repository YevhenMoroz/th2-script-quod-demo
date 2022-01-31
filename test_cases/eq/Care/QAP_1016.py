import logging
from test_framework.core.test_case import TestCase
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
order_type = "Limit"
qty = "900"
price = "20"



class QAP_1016(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        order_book = OMSOrderBook(self.test_id, self.session_id)
        order_ticket  = OMSOrderTicket(self.test_id, self.session_id)
        # endregion
        # region Create CO
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_client_by_name('lookup_1')
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=lookup, recipient=username)
        order_ticket.create_order(lookup=lookup)
        order_id = order_book.extract_field('Order ID')
        # endregion
        # region Check values in OrderBook
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list({"Sts":"Open", "Qty": qty, "Client Name": client, "Limit Price": price})
        # endregion


