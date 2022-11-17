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
from test_framework.rest_api_wrappers.forex.RestApiQuotingSessionMessages import RestApiQuotingSessionMessages


class QAP_T2957(TestCase):
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
        self.rest_massage = RestApiQuotingSessionMessages()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_massage.set_default_params_esp() \
            .enable_always_new_mdentryid() \
            .set_update_type_incremental() \
            .update_parameters({"updateInterval": 30})
        self.rest_manager.send_post_request(self.rest_massage)
        self.sleep(2)
        self.md_request.set_md_req_parameters_maker().change_parameter("MDUpdateType", '1')
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot_inc.set_params_for_md_response(self.md_request)
        self.fix_verifier.check_fix_message(self.md_snapshot_inc)

        self.rest_massage.set_default_params_esp().enable_always_new_mdentryid().set_update_type_fullrefresh()
        self.rest_manager.send_post_request(self.rest_massage)
        self.sleep(2)

        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot_full.set_params_for_md_response(self.md_request)
        self.fix_verifier.check_fix_message(self.md_snapshot_full)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.rest_massage.set_default_params_esp().enable_always_new_mdentryid().set_update_type_fullrefresh()
        self.rest_manager.send_post_request(self.rest_massage)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
