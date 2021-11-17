import logging
import os

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.wrapper_test.DataSet import Connectivity, DirectionEnum
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderList import FixMessageNewOrderList
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from rule_management import RuleManager
from win_gui_modules.application_wrappers import LoginDetailsRequest, OpenApplicationRequest
from custom.basic_custom_actions import create_event
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class Test(TestCase):
    def __init__(self,  report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name

    def qap_4648(self):
        # region create OrderList
        try:
            fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, self.report_id)
            fix_verifier = FixVerifier(Connectivity.Ganymede_317_bs.value, self.report_id)

            new_order_list = FixMessageNewOrderList()
            new_order_list.change_parameters(dict(OrderQty=100000))

            fix_manager.send_message_and_receive_response(new_order_list)
            fix_verifier.check_fix_message(new_order_list, direction=DirectionEnum.SECOND)

            execution_report = FixMessageExecutionReportOMS(new_order_list)
            fix_verifier.check_fix_message(execution_report)
        except:
            logging.error("Error execution", exc_info=True)
        finally:
            RuleManager.remove_rules(rule_list)
        # endregion


    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4648()

