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


class QAP_5593(TestCase):
    def __init__(self, report_id, session_id, date_set):
        super().__init__(report_id, session_id, date_set)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        expected_client = self.data_set.get_client_by_name('client_pt_8')
        fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        fix_message.change_parameter('Account', client)
        fix_manager = FixManager(ss_connectivity, self.case_id)
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = fix_message.get_parameter('Price')
        order_book = OMSOrderBook(self.case_id, self.session_id)
        # endregion

        # region send CO order
        fix_manager.send_message_fix_standard(fix_message)
        # endregion

        # region accept CO order
        client_inbox.accept_order(lookup, qty, price)
        # endregion


        result = order_book.manual_execution(qty, price,
                                             error_expected=True)

        expected_result = {'Trade Ticket Error': 'Error - [QUOD-11750] Manual execution requires Contra Firm'}
        order_book.compare_values(expected_result, result, event_name='Check values')
