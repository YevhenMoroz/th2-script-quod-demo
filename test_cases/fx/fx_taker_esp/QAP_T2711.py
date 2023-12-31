import time
from pathlib import Path

from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2711(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.env.drop_copy, self.test_id)
        self.fix_manager_gtw = FixManager(self.env.buy_side_esp, self.test_id)
        self.qty = random_qty(1, 2, 7)
        self.side = GatewaySide.Sell
        self.status = Status.Fill
        self.account = self.data_set.get_client_by_name("client_1")
        self.new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report_filled_1 = FixMessageExecutionReportAlgoFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters(
            {'TimeInForce': "3", "OrderQty": self.qty, "Account": self.account,
             "DisplayInstruction": {"DisplayQty": "50"}})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2
        self.execution_report_filled_1. \
            set_params_from_new_order_single(self.new_order_sor, self.side, self.status, response=response[-1])
        self.execution_report_filled_1.change_parameter("LastQty", "*")
        self.execution_report_filled_1.update_repeating_group("NoStrategyParameters", "*")
        self.execution_report_filled_1.add_tag({"DisplayInstruction": {"DisplayQty": "50"}})
        self.execution_report_filled_1.remove_parameter("OrderCapacity")
        time.sleep(5)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report_filled_1,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName",
                                                            "trailer", "header"])
        # endregion
