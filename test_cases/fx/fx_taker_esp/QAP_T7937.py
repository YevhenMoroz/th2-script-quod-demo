import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX


class QAP_T3937(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].buy_side_md
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.spot_sec_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {"Symbol": self.eur_usd,
                           "SecurityType": self.spot_sec_type,
                           "Product": "4",
                           "CFICode": "D3",
                           "SecurityIDSource": "8"}
        self.market_id = "D3"
        self.md_req_id = "EUR/USD:SPO:SPO:D3"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_taker()
        self.md_request.change_parameter("MDReqID", self.md_req_id)
        self.md_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Instrument=self.instrument,
                                                        MarketID=self.market_id)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 2
        self.md_reject.set_md_reject_params(self.md_request, text="BAD_NAME")
        self.md_reject.remove_parameter("MDReqRejReason")
        self.fix_verifier.check_fix_message(self.md_reject)
        # endregion


