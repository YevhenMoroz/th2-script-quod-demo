import time
from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_6697(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.symbol = self.data_set.get_symbol_by_name("symbol_3")
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.no_related_symbol = [
            {
                "Instrument": {
                    "Symbol": self.symbol,
                    "SecurityType": "self.security_type",
                    "Product": "4",
                },
                "SettlType": self.settle_type,
            }
        ]
        self.bands = ["1000000", "3000000"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbol)
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 2
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands)
        self.md_snapshot.add_tag({"OrigQuoteEntryID": "*"})
        time.sleep(3)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager.send_message(self.md_request)
