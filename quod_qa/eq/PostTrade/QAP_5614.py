import logging
import os
import time

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.base_window import BaseWindow, decorator_try_except
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixManager import FixManager
from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP5614(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_5614(self):
        # region Declarations
        qty_order = "100"
        price_first_order = "19.2"
        price_second_order = "18.89"
        price_third_order = '19'
        client = "MOClient"
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        base_window = BaseWindow(self.case_id, self.session_id)
        base_window.open_fe(self.session_id, self.report_id, work_dir, username, password)
        # create DMA orders
        oms_order_book = OMSOrderBook(self.case_id, self.session_id)
        oms_middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        fix_manager = FixManager('fix-sell-317-standard-test', self.case_id)
        fix_message_new_order_single = FixMessageNewOrderSingleOMS()
        fix_message_new_order_single.set_default_dma_limit(Instrument.FR0000062788)
        # try:
        #     rule_manager = RuleManager()
        #     nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS', 'XPAR',
        #         float(price_first_order))
        #     nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS', 'XPAR',
        #         float(price_second_order))
        #     nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS', 'XPAR',
        #         float(price_third_order))
        #     trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS',
        #         'XPAR',
        #         float(price_second_order),
        #         float(price_second_order),
        #         int(qty_order),
        #         int(qty_order), delay=0)
        #
        #     trade_rule2 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS',
        #         'XPAR',
        #         float(price_first_order),
        #         float(price_first_order),
        #         int(qty_order),
        #         int(qty_order), delay=0)
        #
        #     trade_rule3 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
        #         'fix-buy-317-standard-test',
        #         'MOClient_PARIS',
        #         'XPAR',
        #         float(price_third_order),
        #         float(price_third_order),
        #         int(qty_order),
        #         int(qty_order), delay=0)
        #     fix_message_new_order_single.change_parameters({"Account": client,
        #                                                     "Price": price_first_order})
        #     fix_manager.send_message(fix_message_new_order_single)
        #     oms_order_book.scroll_order_book(1)
        #     fix_message_new_order_single.change_parameters({"Account": client,
        #                                                     "Price": price_second_order})
        #     fix_manager.send_message(fix_message_new_order_single)
        #     oms_order_book.scroll_order_book(1)
        #     fix_message_new_order_single.change_parameters({"Account": client
        #                                                        , "Price": price_third_order})
        #     fix_manager.send_message(fix_message_new_order_single)
        #     oms_order_book.scroll_order_book(1)
        # finally:
        #     time.sleep(3)
        #     rule_manager.remove_rule(nos_rule1)
        #     rule_manager.remove_rule(nos_rule2)
        #     rule_manager.remove_rule(nos_rule3)
        #     rule_manager.remove_rule(trade_rule1)
        #     rule_manager.remove_rule(trade_rule2)
        #     rule_manager.remove_rule(trade_rule3)
        # endregion

        # region book 1st and 2nd order
        oms_middle_office.set_modify_ticket_details(selected_row_count=2, extract_book=True)
        response = oms_middle_office.book_order()
        print(response)
        response = dict(response)
        # region verify some values
        expected_values = {'book.agreedPrice': '18.94'}
        actually_result = {'book.agreedPrice': response.__getitem__('book.agreedPrice')}
        base_window.compare_values(expected_values, actually_result,
                                   event_name='Check Agreed Price')

        # endregion

        # region mass unbook
        oms_middle_office.mass_un_book([1])
        # endregion

        # region verify Agreed Price
        oms_middle_office.set_modify_ticket_details(selected_row_count=3, extract_book=True)
        response = oms_middle_office.book_order()
        response = dict(response)
        expected_values = {'book.agreedPrice': '19.03'}
        actually_result = {'book.agreedPrice': response.__getitem__('book.agreedPrice')}
        base_window.compare_values(expected_values, actually_result,
                                   event_name='Check Agreed Price')

        # endregion

    def execute(self):
        self.qap_5614()
