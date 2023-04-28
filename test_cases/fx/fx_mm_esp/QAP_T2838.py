from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T2838(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_request_reject = FixMessageMarketDataRequestRejectFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.modify_client_tier = RestApiClientTierMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.md_req_id = f"{self.gbp_usd}:SPO:REG:{self.hsbc}"
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_today = self.data_set.get_settle_date_by_name("today")
        self.settle_type_today = self.data_set.get_settle_type_by_name("today")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.msg_prams = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_fwd,
            "Product": "4"
        }
        self.no_related_symbols = [{
            "Instrument": self.instrument,
            "SettlType": self.settle_type_today, }]
        self.current_time = datetime.now().strftime("%H:%M:%S.%f")
        self.minus_1 = (datetime.now() - timedelta(hours=6))
        self.minus_2 = (datetime.now() - timedelta(hours=5))
        self.timestamp_1 = str(datetime.timestamp(self.minus_1)).replace(".", "")[:13]
        self.timestamp_2 = str(datetime.timestamp(self.minus_2)).replace(".", "")[:13]

        self.minus_3 = (datetime.now() - timedelta(hours=2))
        self.minus_4 = (datetime.now() + timedelta(hours=2))
        self.timestamp_3 = str(datetime.timestamp(self.minus_3)).replace(".", "")[:13]
        self.timestamp_4 = str(datetime.timestamp(self.minus_4)).replace(".", "")[:13]
        self.text = f"11900 Validation failed: current time ({self.current_time}) > end time ({self.minus_1})"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.iridium1)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # region Step 1-2
        self.modify_client_tier.find_client_tier(self.client_id)
        self.msg_prams = self.rest_manager.send_get_request_filtered(self.modify_client_tier)
        self.msg_prams = self.rest_manager.parse_response_details(self.msg_prams, {"clientTierID": self.client_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams) \
            .change_params({"TODStartTime": self.timestamp_1, "TODEndTime": self.timestamp_2})
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.sleep(2)
        # endregion
        # region step 2

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.iridium1). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        position_number = "0"
        bands = []
        for i in response[-1].get_parameter("NoMDEntries"):
            if i["MDEntryPositionNo"] != position_number:
                position_number = i["MDEntryPositionNo"]
                bands.append("*")
        self.md_snapshot.set_params_for_md_response(self.md_request, bands, published=False, response=response[0])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

        # region Step 1-2
        self.modify_client_tier.find_client_tier(self.client_id)
        self.msg_prams = self.rest_manager.send_get_request_filtered(self.modify_client_tier)
        self.msg_prams = self.rest_manager.parse_response_details(self.msg_prams, {"clientTierID": self.client_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams) \
            .change_params({"TODStartTime": self.timestamp_3, "TODEndTime": self.timestamp_4})
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.sleep(2)
        # endregion

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.iridium1). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        position_number = "0"
        bands = []
        for i in response[-1].get_parameter("NoMDEntries"):
            if i["MDEntryPositionNo"] != position_number:
                position_number = i["MDEntryPositionNo"]
                bands.append("*")
        self.md_snapshot.set_params_for_md_response(self.md_request, bands, response=response[0])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.modify_client_tier.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.sleep(2)
