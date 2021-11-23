import logging
import os
import time

from custom import basic_custom_actions as bca, basic_custom_actions
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from datetime import datetime, timedelta
from quod_qa.wrapper_test.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from quod_qa.wrapper_test.oms.FixMessageOrderCancelReplaceRequestOMS import FixMessageOrderCancelReplaceRequestOMS
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP2002(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_2002(self):
        rule_manager = RuleManager()
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        # region Declarations
        client = "CLIENT1"
        price = '20'
        fix_message = FixMessageNewOrderSingleOMS()
        fix_message.set_default_dma_market(Instrument.FR0004186856)
        fix_message.change_parameters({'Account': client, 'TimeInForce': '4'})
        fix_message.add_ClordId(os.path.basename(__file__)[:-3])
        # endregion
        # region Create order via FIX
        try:
            nos_rule = rule_manager.add_MarketNewOrdSingle_FOK_FIXStandard(self.bs_connectivity,
                                                                           'XPAR_' + client, 'XPAR',
                                                                           float(price), True)
            fix_manager.send_message_and_receive_response_fix_standard(fix_message)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region checkCancel
        execution_status_trade = FixMessageExecutionReportOMS()
        execution_status_trade.set_default_filled()
        execution_status_trade.remove_parameter('Price')
        execution_status_trade.change_parameters(
            {'ClOrdID': fix_message.get_parameter('ClOrdID')})
        fix_verifier.check_fix_message_fix_standard(execution_status_trade, ['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_2002()
