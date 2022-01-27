import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_6181(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_6181(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        fix_manager = FixManager(self.ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit()
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = fix_message.get_parameter('Price')
        type = "Limit"
        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion

        # # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        # endregion

        # region accept CO orders
        client_inbox.accept_order('O', 'M', 'S')
        # endregion

        # region split order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             'XPAR_' + fix_message.get_parameter(
                                                                                                 'Account'),
                                                                                             'XPAR', float(price))
            order_book.set_order_ticket_details(qty, type, price)
            order_book.split_limit_order()

        except Exception:
            logger.debug('Good Job, Oleg')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region send modify request
        try:
            rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity, 'XPAR_' +
                                                                   fix_message.get_parameter('Account'), 'XPAR', True)
            fix_message_cancer_replace = FixMessageOrderCancelReplaceRequestOMS(fix_message.get_parameters())
            fix_message_cancer_replace.change_parameter('OrderQtyData', {'OrderQty': '50'})
            fix_message_cancer_replace.add_tag({'OrigClOrdID': fix_message.get_parameter("ClOrdID")})
            fix_manager.send_message_fix_standard(fix_message_cancer_replace)
            # region accept modify
            client_inbox.accept_modify_plus_child('O', 'M', 'S')
            # endregion
        except Exception:
            logger.debug('Error Message' + {Exception})
        finally:
            time.sleep(3)

        # endregion

        # region verify order
        result = order_book.extract_2lvl_fields('Child Orders', ['Qty', 'Sts'], [1])
        order_book.compare_values({'Qty': '50', 'Sts': 'Open'}, result[0], 'Compare Value')
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_6181()
