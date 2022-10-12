from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2533(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fix_manager = FixManager(self.connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.settle_date = self.data_set.get_settle_date_by_name("broken_1")
        self.settle_type = self.data_set.get_settle_type_by_name("broken")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.venue = self.data_set.get_venue_by_name("venue_3")
        self.market_id = self.data_set.get_market_id_by_name("market_3")
        self.qty = "3000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type
        }
        self.status_new = Status.Pending

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.new_order.set_default_SOR().change_parameters({"Instrument": self.instrument,
                                                            "SettlDate": self.settle_date,
                                                            "SettlType": self.settle_type,
                                                            "OrderQty": self.qty})
        self.fix_manager.send_message_and_receive_response(self.new_order)
        # endregion
        # Region Step 2
        self.execution_report.set_params_from_new_order_single(self.new_order, status=self.status_new)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
