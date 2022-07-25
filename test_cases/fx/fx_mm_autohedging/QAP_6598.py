import time
from pathlib import Path

from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker

qty = random_qty(1, 2, 7)
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell
status = DataSet.Status.Fill


class QAP_6598(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.fix_manager_gtw = FixManager(self.ss_t_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.account = self.data_set.get_client_by_name("client_int_1")

    def run_pre_conditions_and_steps(self):
        # region Step 1
        new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set).set_default_mo().change_parameters(
            {'TimeInForce': "3", "OrderQty": qty, "Account": self.account})
        new_order_sor.add_tag({"ExDestination": "CITI-SW"})
        self.fix_manager_gtw.send_message_and_receive_response(new_order_sor)
        # endregion
        # region Step 2-3
        execution_report_filled = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_sor, gateway_side_buy, status)
        execution_report_filled.change_parameter("LastQty", "*")
        execution_report_filled.remove_parameter("Account")
        time.sleep(5)
        self.fix_verifier.check_fix_message(fix_message=execution_report_filled,
                                            direction=DirectionEnum.FromQuod)

        new_order_ah = FixMessageNewOrderSingleTaker().set_default_SOR().change_parameters(
            {'TimeInForce': "0", "OrderQty": qty, "OrdType": "1"})
        execution_report_ah = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_ah, gateway_side_sell, status)
        execution_report_ah.remove_parameters(["Price", "Account", "NoStrategyParameters"])
        execution_report_ah.add_tag({"LastMkt": "*"})
        key_params = ["OrdStatus", "OrderQty", "OrderID", "Side"]
        execution_report_ah.change_parameters({"LastQty": "*", "ClOrdID": "*", "Side": "2"})
        self.fix_verifier.check_fix_message(fix_message=execution_report_ah, key_parameters=key_params,
                                            direction=DirectionEnum.FromQuod, message_name="Check AutoHedger Report")
        # endregion
