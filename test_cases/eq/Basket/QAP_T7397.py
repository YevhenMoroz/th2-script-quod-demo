import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7397(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.fe_env = environment.get_list_fe_environment()[0]
        self.user1 = self.fe_env.user_1
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send NewOrderSingle
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_manager.send_message_and_receive_response_fix_standard(nos)
        cl_id = nos.get_parameter("ClOrdID")
        # endregion
        # region Accept
        self.cl_inbox.accept_order()
        # endregion
        # region ReOrder
        self.order_ticket.set_order_details(recipient=self.user1, partial_desk=True)
        self.order_ticket.re_order()
        # endregion
        # region ManualExecute
        self.order_book.manual_execution()
        # endregion
        # region Verify context menu
        act_result = self.order_book.is_menu_item_present("Create Basket", [1, 2])
        print(act_result)
        self.order_book.compare_values({"isMenuItemPresent": "false"}, {"isMenuItemPresent": act_result}, "Verify context menu")
        # endregion
