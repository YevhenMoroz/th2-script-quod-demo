import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2498(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.result = str()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data(). \
            update_value_in_repeating_group("NoMDEntries", "MDQuoteType", '0'). \
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD IND")

        # region Step 3
        md_req_id = self.fix_md.get_parameters()["MDReqID"]
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FXFH.log",
                                                         rf"^.*{md_req_id}.*MDQuoteType=Indicative.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "failed"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"MDQuoteType=Indicative\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data(). \
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD TRD")
        time.sleep(4)
        md_req_id = self.fix_md.get_parameters()["MDReqID"]
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FXFH.log",
                                                         rf"^.*{md_req_id}.*MDQuoteType=Tradeable.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "failed"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"MDQuoteType=Tradeable\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()

