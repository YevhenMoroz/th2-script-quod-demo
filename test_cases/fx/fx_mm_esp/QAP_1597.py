from test_framework.core.environment import Environment
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from pathlib import Path
from test_framework.data_sets.constants import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX


class QAP_1597(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: Environment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.symbol = "EUR/sdf"
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.text = "no active client tier"
        self.no_related_symbol = [
            {
                "Instrument": {
                    "Symbol": self.symbol,
                    "SecurityType": self.security_type,
                    "Product": "4",
                },
                "SettlType": self.settle_type,
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.no_related_symbol)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request)
        # endregion
        # region Step 2
        self.md_reject.set_md_reject_params(self.md_request, text=self.text)
        self.fix_verifier.check_fix_message(self.md_reject, direction=DirectionEnum.FromQuod)
        # endregion
