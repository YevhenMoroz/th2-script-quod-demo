import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_T7197(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.expected_client = self.data_set.get_client_by_name('client_pt_8')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('Account', self.client)
        self.fix_manager = FixManager(ss_connectivity, self.test_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion

        # region accept CO order
        self.client_inbox.accept_order(self.lookup, self.qty, self.price)
        # endregion

        result = self.order_book.manual_execution(self.qty, self.price,
                                             error_expected=True)

        expected_result = {'Trade Ticket Error': 'Error - [QUOD-11750] Manual execution requires Contra Firm'}
        self.order_book.compare_values(expected_result, result, event_name='Check values')
