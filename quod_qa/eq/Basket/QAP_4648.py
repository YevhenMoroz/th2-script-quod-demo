import logging
import os

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP4648(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_4648(self):
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.bs_connectivity, self.report_id)
        # region create OrderList
        new_order_list = FixMessageNewOrderListOMS().set_default_order_list()
        fix_manager.send_message_and_receive_response_fix_standard(new_order_list)
        # fix_verifier.check_fix_message_fix_standard(new_order_list, direction=DirectionEnum.SECOND)
        # list_status = FixMessageListStatus(new_order_list)
        # fix_verifier.check_fix_message_fix_standard(list_status)

        # endregion

    #@decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4648()
