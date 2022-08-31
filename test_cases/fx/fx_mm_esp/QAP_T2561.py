from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2561(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.book_type_tiered = "1"
        self.sweepable_bands = ["2000000", "6000000", "12000000"]
        self.tiered_bands = ["1000000", "2000000"]
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.eur_usd,
                "SecurityType": self.sec_type_spot,
                "Product": "4"
            },
            "SettlType": self.settle_type_spot
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium1)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, self.sweepable_bands)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameters({"SenderSubID": self.palladium1,
                                                                         "BookType": self.book_type_tiered})
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, self.tiered_bands)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
