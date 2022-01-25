import logging

from datetime import datetime
from test_framework.core.test_case import TestCase
from test_framework.old_wrappers import eq_wrappers
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


from custom.basic_custom_actions import create_event, timestamps

from rule_management import RuleManager
from stubs import Stubs
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
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
instrument = "VETO"


class QAP_1016(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    def run_pre_conditions_and_steps(self):
        case_name = "QAP-1016"
        seconds, nanos = timestamps()  # Store case start time
        # region Declarations
        time = datetime.utcnow().isoformat()

        base_window = BaseMainWindow(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        order_ticket  = OMSOrderTicket(self.test_id, self.session_id)
        # endregion
        # region Open FE
        session_id = set_session_id()
        case_id = create_event(case_name, self.report_id)
        # case_id = create_event(case_name, report_id)
        # set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)


        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region Create CO

        client = self.data_set.get_client_by_name('client_co_1')
        # eq_wrappers.create_order(base_request, , , lookup, , is_care=True, ,
        #                         , recipient_user=True)
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=instrument, recipient=username)
        order_ticket.create_order(lookup=instrument)

        order_id = order_book.extract_field('Order ID')
        # endregion
        # region Check values in OrderBook

        order_book.set_filter(['Order ID', order_id]).check_order_fields_list({"Sts":"Open", "Qty": qty, "Client Name": client, "Limit Price": price})

        # endregion

        logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
