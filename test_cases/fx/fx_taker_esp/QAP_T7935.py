from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T7935(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].buy_side_md
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.uss_myr = self.data_set.get_symbol_by_name("unsupported_symbol")
        self.security_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.market_id_hsbc_sw = self.data_set.get_market_id_by_name("market_2")
        self.rand_id = bca.client_orderid(3)
        self.md_req_id = f"{self.uss_myr}:SPO:REG:{self.venue}_{self.rand_id}"

        self.instrument = {
            "SecurityIDSource": "8",
            "CFICode": self.market_id_hsbc_sw,
            "Symbol": self.uss_myr,
            "SecurityType": self.security_type_spo,
            "Product": "4"
        }
        self.no_related_symbols = [{
            "Instrument": self.instrument,
            "SettlDate": self.settle_date_spot,
            "SettlType": self.settle_type_spot,
            "MarketID": self.market_id_hsbc_sw
        }]
        self.bands = []
        self.text = "no listing found"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_taker().change_parameter("MDReqID", self.md_req_id)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
        # region step 2-3
        self.md_reject.set_md_reject_params(self.md_request, text=self.text)
        self.md_reject.change_parameter("MDReqRejReason", "0")
        self.fix_verifier.check_fix_message(self.md_reject, key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
