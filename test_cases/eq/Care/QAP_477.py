import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsMic, OmsVenueClientNames
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_477(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.username = Stubs.custom_config['qf_trading_fe_user']
        self.password = Stubs.custom_config['qf_trading_fe_password']
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.ord_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.order_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.rule_manager = RuleManager()
        self.fix_manager = FixManager(self.ss_connectivity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                              self.venue_client_names,
                                                                                              self.venue,
                                                                                              float(self.price))
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.route = self.data_set.get_route("route_1")
        self.price = self.fix_message.get_parameter('Price')
        self.qty = '100'
        self.limit = '10'
        self.instr = 'VETO'


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region Create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id_first = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Accept CO order
        self.order_inbox.accept_order(self.instr, self.qty, self.limit)
        # endregion
        # region DirectLoc order
        try:
            self.order_book.direct_loc_order_correct(self.fix_message.get_parameter('OrderQtyData')['OrderQty'], self.route)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            self.rule_manager.remove_rule(self.nos_rule)
        # endregion
        # region extraction_value
        result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value, [OrderBookColumns.sts.value, OrderBookColumns.qty.value], rows=[1],
                                                filter_dict={OrderBookColumns.order_id.value: order_id_first})
        self.base_window.compare_values({OrderBookColumns.sts.value: ExecSts.open.value, OrderBookColumns.qty.value: self.qty}, result[0], 'Equals value')
        # endregion



