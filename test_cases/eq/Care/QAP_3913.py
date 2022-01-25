import datetime
import logging
import os
import time

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.old_wrappers.eq_wrappers import manual_match
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_3913(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.act_java_api = Stubs.act_java_api
        self.connectivity = '317_java_api'

    def qap_3913(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        trade_book = OMSTradesBook(self.case_id, self.session_id)
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_message = FixMessageNewOrderSingleOMS()
        fix_message.set_default_care_limit()
        qty = fix_message.get_parameter('OrderQtyData')["OrderQty"]
        price = fix_message.get_parameter('Price')
        client = 'MOClient'
        fix_message.change_parameter('Account', client)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion

        # region create CO order via FIX
        fix_manager.send_message_fix_standard(fix_message)
        # order_book.scroll_order_book(1)
        order_id = order_book.extract_field('Order ID')
        order_inbox.accept_order("O", "M", "S")
        # endregion
        fix_message.set_default_dma_limit()
        fix_message.change_parameter('Account', client)
        # region create DMA order via FIX
        valeron = None
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager. \
                add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                         client + "_PARIS", 'XPAR', float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_PARIS",
                                                                                       'XPAR', float(price),
                                                                                       int(qty), 0)
            fix_manager.send_message_and_receive_response_fix_standard(fix_message)
        except Exception:
            logger.error({Exception})

        finally:
            time.sleep(7)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)

        exec_id = order_book.extract_2lvl_fields('Executions', ['ExecID'], [1])[0]['ExecID']
        # endregion

        trade_book.manual_match(qty_to_match=qty, order_filter_list=['OrderId', order_id],
                                trades_filter_list=['ExecID', exec_id])
        exec_id_care = order_book.extract_2lvl_fields('Executions', ['ExecID'], [1], {'Order ID': order_id})[0][
            'ExecID']
        order_book.set_filter(['Order ID', order_id])
        unmatched_qty = order_book.extract_field('UnmatchedQty')
        order_book.compare_values({'Value': '0'}, {'Value': unmatched_qty}, 'Verifier1')
        unmatch_params = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'UnMatchRequestBlock': {
                'UnMatchingList': {'UnMatchingBlock': [
                    {'VirtualExecID': exec_id_care, 'UnMatchingQty': qty}
                ]},
            }
        }
        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_UnMatchRequest', unmatch_params, self.connectivity),
            parent_event_id=self.case_id
        ))
        order_book.set_filter(['Order ID', order_id])
        unmatched_qty = order_book.extract_field('UnmatchedQty')
        order_book.compare_values({'Value': '100'}, {'Value': unmatched_qty}, 'Verifier2')
        trade_book.manual_match(qty_to_match=qty, order_filter_list=['OrderId', order_id],
                                trades_filter_list=['ExecID', exec_id])
        order_book.set_filter(['Order ID', order_id])
        unmatched_qty = order_book.extract_field('UnmatchedQty')
        order_book.compare_values({'Value': '0'}, {'Value': unmatched_qty}, "Verifier3")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3913()
