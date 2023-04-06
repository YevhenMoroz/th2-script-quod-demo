import os
import re
from datetime import datetime
from pathlib import Path

from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.ssh_wrappers.ssh_client import SshClient



class QAP_T9371(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.verifier = Verifier()
        self.key = None
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.acc_iridium = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.gbp_usd_spot = {
            'Symbol': self.gbp_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.gbp_usd_spot,
            'SettlType': self.settle_type_spot}]
        self.md_symbol_spo = 'GBP/USD:SPO:REG:HSBC'
        self.no_md_entries_spot = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19599,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19810,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]
        # region SSH
        self.temp_path = "C:/Users/amedents/PycharmProjects/th2-script-quod-demo/temp"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.acc_iridium)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message(self.md_request)

        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_symbol_spo, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(10)
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region precondition: Prepare QS configuration
        self.ssh_client.get_file("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
                                 self.temp_path)
        self.ssh_client.close()
        logs = open(self.temp_path, "r")
        for line in logs:
            self.key = re.findall(r"\)\s*-\s*data\s+is\s+a\s+duplicate$", line)
            if self.key:
                self.key = "data is a duplicate"
                break
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Find \"data is a duplicate\" message")
        self.verifier.compare_values("Free notes", "data is a duplicate", self.key)
        self.verifier.verify()
        logs.close()
        os.remove(self.temp_path)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_symbol_spo, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(2)
