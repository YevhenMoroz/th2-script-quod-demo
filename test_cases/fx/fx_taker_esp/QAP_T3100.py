import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T3100(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.md_taker_connectivity = self.environment.get_list_fix_environment()[0].buy_side_md
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_gtw = FixManager(self.md_taker_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.md_taker_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_request_fwd = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.md_snapshot_fwd = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")

        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")

        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_fwd = self.data_set.get_settle_date_by_name("wk1")
        self.settle_type_fwd = self.data_set.get_settle_type_by_name("wk1")

        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.market_id = self.data_set.get_market_id_by_name("market_1")
        self.rand_id = bca.client_orderid(3)

        self.md_id = f"{self.symbol}:SPO:REG:{self.venue}_{self.rand_id}"
        self.md_req_id = f"{self.symbol}:SPO:REG:{self.venue}"

        self.md_id_fwd = f"{self.symbol}:FXF:WK1:{self.venue}_{self.rand_id}"
        self.md_req_id_fwd = f"{self.symbol}:FXF:WK1:{self.venue}"

        self.instrument = {
            "SecurityIDSource": "8",
            "CFICode": self.market_id,
            "Symbol": self.symbol,
            "SecurityType": self.security_type,
            "Product": "4"
        }
        self.no_related_symbols = [{
            "Instrument": self.instrument,
            "SettlType": self.settle_type,
            "MarketID": self.market_id
        }]

        self.instrument_fwd = {
            "SecurityIDSource": "8",
            "CFICode": self.market_id,
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd,
            "Product": "4"
        }
        self.no_related_symbols_fwd = [{
            "Instrument": self.instrument,
            "SettlDate": self.settle_date_fwd,
            "MarketID": self.market_id
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_taker().change_parameter("MDReqID", self.md_id)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion

        # region step 2
        self.md_snapshot.set_params_for_md_response_taker_spo(self.md_request, ["*", "*", "*"])
        time.sleep(1)
        self.md_snapshot.change_parameters({"SettlDate": self.settle_date,
                                            "MDReqID": self.md_id})
        self.md_snapshot.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "SettlDate"])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion

        # region step 3
        self.md_request_fwd.set_md_req_parameters_taker().change_parameter("MDReqID", self.md_req_id_fwd)
        self.md_request_fwd.update_repeating_group("NoRelatedSymbols", self.no_related_symbols_fwd)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request_fwd, self.test_id)
        # endregion

        # region step 4
        self.md_snapshot_fwd.set_params_for_md_response_taker_wk1(self.md_request_fwd, ["*"])
        time.sleep(1)
        self.md_snapshot.change_parameters({"SettlDate": self.settle_date_fwd,
                                            "MDReqID": self.md_id_fwd})
        self.md_snapshot_fwd.remove_parameters(["OrigMDArrivalTime", "OrigMDTime"])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot_fwd)
        self.md_request_fwd.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request_fwd, self.test_id)
        # endregion
