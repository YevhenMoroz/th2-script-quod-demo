import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import PercentageProfile
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_4021(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.case_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_manager.send_message_and_receive_response_fix_standard(nol)
        # endregion
        # region Accept
        lookup = self.data_set.get_lookup_by_name("lookup_1")
        qty1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["OrderQtyData"]["OrderQty"]
        qty2 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["OrderQtyData"]["OrderQty"]
        price1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["Price"]
        price2 = nol.get_parameter("ListOrdGrp")['NoOrders'][1]["Price"]
        self.cl_inbox.accept_order(lookup, qty1, price1)
        self.cl_inbox.accept_order(lookup, qty2, price2)
        # endregion

        self.basket_book.wave_basket("50", PercentageProfile.remaining_qty,self.data_set.get_route("route_1"))
        self.basket_book.extract


