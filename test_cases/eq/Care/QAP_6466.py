import logging
import os
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import \
    FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_6466(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.qty = "100"
        self.price = "50"
        self.sts = "PCA"
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.venue_client_name = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.case_id = create_event(self.__class__.__name__, self.report_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.nos_rule = None
        self.cancel_replace_rule = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.__send_fix_order()
        self.cl_inbox.accept_order(self.data_set.get_lookup_by_name("lookup_1"), self.qty, self.price)
        self.order_ticket.set_order_details(qty=self.qty)
        self.order_ticket.split_order()
        self.__send_cancel_request()
        self.cl_inbox.accept_and_cancel_children(self.data_set.get_lookup_by_name("lookup_1"), self.qty, self.price)
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: self.sts})

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        if self.nos_rule:
            self.rule_manager.remove_rule(self.nos_rule)

    def __send_fix_order(self):
        self.nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
            self.fix_env.buy_side, self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1"),
            self.data_set.get_mic_by_name("mic_1"), float(self.price))
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client})
        self.fix_manager.send_message_fix_standard(self.new_order_single)

    def __send_cancel_request(self):
        cancel_request = FixMessageOrderCancelRequestOMS().set_default(self.new_order_single).add_ClordId(
            (os.path.basename(__file__)[:-3]))
        self.fix_manager.send_message_fix_standard(cancel_request)
