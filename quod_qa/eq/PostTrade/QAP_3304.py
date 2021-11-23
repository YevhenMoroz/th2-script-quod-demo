import logging
import os
import time

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP3304(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_3304(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        ord_book = OMSOrderBook(self.case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        qty = "100"
        price = "20"
        # endregion
        # region Open FE
        ord_book.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderSingle
        nos = FixMessageNewOrderSingleOMS().set_default_dma_limit()
        client = nos.get_parameters()["Account"]
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             'XPAR_' + client, "XPAR",
                                                                                             float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       'XPAR_' + client, 'XPAR',
                                                                                       float(price), int(qty), 1)
            fix_manager.send_message_and_receive_response_fix_standard(nos)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion
        # region Book Order
        middle_office.book_order()
        # endregion
        # region Check OrderBook
        ord_book.scroll_order_book()
        post_trd_sts = ord_book.extract_field("PostTradeStatus")
        ord_book.compare_values({'PostTradeStatus': "Booked"}, {'PostTradeStatus': post_trd_sts},
                                "Check PostTradeStatus")
        # endregion
        # region Check MiddleOffice
        block_sts = middle_office.extract_block_field("Status")
        block_match_sts = middle_office.extract_block_field("Match Status")
        middle_office.compare_values({'Status': "ApprovalPending", 'Match Status': "Unmatched"},
                                     {'Status': block_sts['Status'], 'Match Status': block_match_sts['Match Status']},
                                     "Check block")
        # endregion
        # region UnBook
        middle_office.un_book_order()
        # endregion
        # region Check OrderBook
        post_trd_sts = ord_book.extract_field("PostTradeStatus")
        ord_book.compare_values({'PostTradeStatus': "ReadyToBook"}, {'PostTradeStatus': post_trd_sts},
                                "Check PostTradeStatus")
        # endregion
        # region Check MiddleOffice
        block_sts = middle_office.extract_block_field("Status")
        block_match_sts = middle_office.extract_block_field("Match Status")
        middle_office.compare_values({'Status': "Canceled", 'Match Status': "Unmatched"},
                                     {'Status': block_sts['Status'], 'Match Status': block_match_sts['Match Status']},
                                     "Check block")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3304()
