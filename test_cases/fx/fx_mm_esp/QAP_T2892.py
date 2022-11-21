from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum, Status
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2892(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX()
        self.new_order_single = FixMessageNewOrderSingleFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.status_reject = Status.Reject
        self.qty58m = "58000000"
        self.bands_eur_usd = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium1)

        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        number_of_bands = len(response[0].get_parameter("NoMDEntries")) / 2
        for i in range(int(number_of_bands)):
            self.bands_eur_usd.append("*")
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

        # region step 2
        self.new_order_single.set_default().change_parameters(
            {"Account": self.palladium1, "OrderQty": self.qty58m})
        for i in self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id):
            if i.get_parameter("OrdStatus") == "8":
                response = i
        # endregion

        # region step 3
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.status_reject,
                                                               response=response)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
