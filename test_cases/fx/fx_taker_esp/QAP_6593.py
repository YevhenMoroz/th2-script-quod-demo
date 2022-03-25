import time
from pathlib import Path

from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

qty = random_qty(1, 2, 7)
gateway_side_sell = GatewaySide.Sell
status = Status.Fill


class QAP_6593(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_t_connectivity = None
        self.dc_connectivity = None
        self.fix_manager_gtw = None
        self.fix_verifier = None

    def run_pre_conditions_and_steps(self):
        # region Initialization
        self.ss_t_connectivity = SessionAliasFX().ss_esp_t_connectivity
        self.dc_connectivity = SessionAliasFX().dc_connectivity
        self.fix_manager_gtw = FixManager(self.ss_t_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        # endregion
        # region Variables
        account = self.data_set.get_client_by_name("client_1")
        # endregion
        # region Step 1
        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'TimeInForce': "3", "OrderQty": qty, "Account": account})
        self.fix_manager_gtw.send_message_and_receive_response(new_order_sor)
        # endregion
        # region Step 2
        execution_report_filled_1 = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_sor, gateway_side_sell, status)
        execution_report_filled_1.change_parameter("LastQty", "*")
        execution_report_filled_1.remove_parameter("Account")
        execution_report_filled_1.update_repeating_group("NoStrategyParameters", "*")
        time.sleep(5)
        self.fix_verifier.check_fix_message(fix_message=execution_report_filled_1,
                                            direction=DirectionEnum.FromQuod)
        # endregion
