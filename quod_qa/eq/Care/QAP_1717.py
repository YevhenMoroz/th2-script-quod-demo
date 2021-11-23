import logging
import os
import time

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP1717(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_1717(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        ord_book = OMSOrderBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        lokup = "VETO"
        qty = "100"
        price = "20"
        # endregion
        # region Open FE
        cl_inbox.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderSingle
        nos = FixMessageNewOrderSingleOMS().set_default_care_limit()
        fix_manager.send_message_and_receive_response_fix_standard(nos)
        client = nos.get_parameters()["Account"]
        # endregion
        # region Direct orders
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             "XPAR_" + client, "XPAR",
                                                                                             float(price))
            cl_inbox.direct_order(lokup, qty, price, "100")
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
        # endregion
        #region Check child
        ord_book.scroll_order_book()
        child_ord_detail = ord_book.extract_2lvl_fields("Child Orders", ["Sts", "Qty", "Limit Price"], [1])
        ord_book.compare_values({'Sts': "Open", 'Qty': qty, "Price": price}, child_ord_detail[0], "Check Child")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_1717()
