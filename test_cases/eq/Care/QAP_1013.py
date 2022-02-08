import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# region TestData


class QAP_1013(TestCase):
    def __init__(self, report_id, session_id, dataset):
        super().__init__(report_id, session_id, dataset)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        order_book = OMSOrderBook(self.case_id, self.session_id)
        client = self.data_set.get_client_by_name('client_pt_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        price = '100'
        qty = '100'
        user = Stubs.custom_config['qf_trading_fe_user']
        order_ticket.set_order_details(client=client, limit=price, qty=qty, tif='Day', recipient=user,
                                       partial_desk=True
                                       )
        order_ticket.create_order(self.data_set.get_lookup_by_name('lookup_1'))
        order_id = order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion

        # region reject CO order
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_inbox.reject_order(lookup, qty, price)
        # endregion

        # region verify Sts of order
        order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        sts = order_book.extract_field(OrderBookColumns.sts.value)
        order_book.compare_values({OrderBookColumns.sts.value: ExecSts.rejected.value}, {OrderBookColumns.sts.value: sts},
                                  'Verifier data')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
