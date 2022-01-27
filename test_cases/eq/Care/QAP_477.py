import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsMic, OmsVenueClientNames
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# region TestData
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity

qty = '100'
limit = '10'
instr = 'VETO'



# endregion


class QAP_477(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.test_id, self.session_id)
        ord_ticket = OMSOrderTicket(self.test_id, self.session_id)
        base_window = BaseMainWindow(self.test_id, self.session_id)
        fix_manager = FixManager(ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        # endregion
        # region Create CO order
        fix_manager.send_message_fix_standard(fix_message)
        order_id_first = order_book.extract_field('Order ID')
        # endregion
        # region Accept CO order
        order_inbox = OMSClientInbox(self.test_id, self.session_id)
        order_inbox.accept_order(instr, qty, limit)
        # endregion
        # region DirectLoc order
        price = fix_message.get_parameter('Price')
        try:
            rule_manager = RuleManager()
            venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
            venue = self.data_set.get_mic_by_name("mic_1")
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                             venue_client_names, venue,
                                                                                             float(price))
            route = self.data_set.get_route("route_1")
            order_book.direct_loc_order_correct(fix_message.get_parameter('OrderQtyData')['OrderQty'], route)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            rule_manager.remove_rule(nos_rule)
        # endregion
        # region extraction_value
        result = order_book.extract_2lvl_fields('Child Orders', ['Sts', 'Qty'], rows=[1],
                                                filter_dict={'Order ID': order_id_first})
        base_window.compare_values({'Sts': 'Open', 'Qty': qty}, result[0], 'Equals value')
        # endregion



