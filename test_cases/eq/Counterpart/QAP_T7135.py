import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7135(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_1")
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_ticket.set_order_details(client=self.client, limit="10", qty="100",
                                            account=self.account)
        self.order_ticket.create_order(self.lookup)
        self.order_book.check_order_fields_list({OrderBookColumns.custodian.value: "Custodian - Acc1SubAcc1"})
        # endregion
        # region Step 2
        self.order_ticket.set_order_details(client=self.client, limit="10", qty="100",
                                            account=self.account)
        self.order_ticket.set_parties_tab_details(custodian="Custodian - Acc2SubAcc1")
        self.order_ticket.create_order(self.lookup)
        self.order_book.check_order_fields_list({OrderBookColumns.custodian.value: "Custodian - Acc2SubAcc1"})
        # endregion
