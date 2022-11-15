from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportTakerMO import FixMessageExecutionReportTakerMO
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T8666(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.esp_t_connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportTakerMO()
        self.venue_d3 = self.data_set.get_venue_by_name("venue_9")
        self.rejected = Status.Reject
        self.text = "11615 'VenueID': D3 not tradable"
        self.qty = "1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.new_order.set_default_mo()
        self.new_order.change_parameters({"ExDestination": self.venue_d3})
        self.fix_manager.send_message_and_receive_response(self.new_order)
        # endregion
        # regions Step 2
        self.execution_report.set_params_from_new_order_single(self.new_order, status=self.rejected)
        self.execution_report.change_parameters({"Text": self.text})
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
