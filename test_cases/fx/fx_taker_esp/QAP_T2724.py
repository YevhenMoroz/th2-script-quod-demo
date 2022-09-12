import time
from pathlib import Path
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2724(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.buy_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.buy_side_esp, self.test_id)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.status = Status.Reject
        self.account = self.data_set.get_client_by_name("client_1")
        self.instrument = dict(
            Symbol=self.data_set.get_symbol_by_name('symbol_1'),
            SecurityType=self.data_set.get_security_type_by_name('fx_spot')
        )
        self.qty = random_qty(1, 2, 7)

    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters({"Instrument": self.instrument, "TimeInForce": "0",
                                                                "OrdType": "4", "OrderQty": self.qty,
                                                                "Account": self.account})
        self.new_order_sor.add_tag({"StopPx": "2"})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2-3
        self.execution_report.set_params_from_new_order_single(self.new_order_sor, status=self.status)
        self.execution_report.change_parameter("Text", "11605 'StopPrice' (2) greater than 'Price' (1.18999)")
        self.execution_report.change_parameters({"LastQty": "*",
                                                 "Account": self.account,
                                                 "HandlInst": "*",
                                                 "OrdRejReason": "*",
                                                 "StopPx": "2",
                                                 "StrategyName": "*",
                                                 "TargetStrategy": "*",
                                                 "NoStrategyParameters": "*"})
        self.execution_report.remove_parameters(["LastMkt", "ExecRestatementReason", "SettlType",
                                                 "SettlCurrency", "OrderCapacity"])
        time.sleep(5)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
