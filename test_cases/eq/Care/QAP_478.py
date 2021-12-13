import logging
import os
import time
from rule_management import RuleManager
from test_framework.win_gui_wrappers.base_window import decorator_try_except

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_478(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_478(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        route = 'Route via FIXBUYTH2 - component'
        fix_manager = FixManager(self.ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit()
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        client = fix_message.get_parameter('Account')
        print(qty)
        print(client)

        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        order_id_first = order_book.extract_field('Order ID')
        # endregion

        # region accept CO order
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_inbox.accept_order('O', 'M', 'S')
        # endregion
        rule_manager = RuleManager()
        # region directLoc order
        try:
            nos_rule = rule_manager.add_NewOrdSingle_Market_FIXStandard(self.bs_connectivity,
                                                                        'XPAR_' + client,
                                                                        'XPAR', False, int(qty),
                                                                        float(fix_message.get_parameter('Price')))

            order_book.direct_moc_order_correct(qty, route)
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            time.sleep(3)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region extraction_value
        result = order_book.extract_2lvl_fields('Child Orders', ['Sts', 'Qty'], rows=[1],
                                                filter_dict={'Order ID': order_id_first})

        base_window.compare_values({'Sts': 'Eliminated', 'Qty': '100'}, result[0], 'Equals value')

        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_478()
