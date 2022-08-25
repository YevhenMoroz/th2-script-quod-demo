from pathlib import Path
from time import sleep

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.data_sets.constants import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataIncrementalRefreshSellFX import \
    FixMessageMarketDataIncrementalRefreshSellFX
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2430(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_snapshot_full = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.md_snapshot_inc = FixMessageMarketDataIncrementalRefreshSellFX()
        self.rest_manager = RestApiManager(self.adm_env.session_alias_wa, self.test_id)
        self.rest_message = RestApiClientTierInstrSymbolMessages()
        self.client_tier_silver = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.client_silver = self.data_set.get_client_by_name("client_mm_1")
        self.aud_usd = self.data_set.get_symbol_by_name("symbol_16")
        self.qty_list = ['1000000', '5000000', '10000000', '6000000']
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.aud_usd,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
        }]
        self.params = {}


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Set params for client tier
        self.rest_message.find_all_client_tier_instrument()
        self.params = self.rest_manager.send_get_request(self.rest_message)
        self.params = self.rest_manager. \
            parse_response_details(self.params,
                                   {'clientTierID': self.client_tier_silver, 'instrSymbol': self.aud_usd})
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params).set_sweepable_qty(self.qty_list[:3])
        self.rest_manager.send_post_request(self.rest_message)
        # endregion
        # region subscription to the updated instrument
        self.md_request.set_md_req_parameters_maker().add_tag(
            {
                "SenderSubID": self.client_silver,
                'NoRelatedSymbols': self.no_related_symbols
            })
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot_full.set_params_for_md_response(self.md_request, self.qty_list[:3])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot_full,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        # region unsubscribe
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
        # endregion
        # region Set default params
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params).add_tenor_qty(self.qty_list[3:])
        self.rest_manager.send_post_request(self.rest_message)
        # endregion
        # region Checking default params
        self.md_request.add_tag(
            {
                "MDReqID": bca.client_orderid(10),
                "SubscriptionRequestType": "1"
            }
        )
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot_full.set_params_for_md_response(self.md_request, self.qty_list)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot_full,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        # region Set default params
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params).add_tenor_qty(self.qty_list[:3])
        self.rest_manager.send_post_request(self.rest_message)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region unsubscribe
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
        # endregion

