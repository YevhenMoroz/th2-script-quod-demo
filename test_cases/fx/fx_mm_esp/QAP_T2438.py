import time
from pathlib import Path
from pkg_resources import resource_filename
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
from test_framework.ssh_wrappers.ssh_client import SshClient
from xml.etree.ElementTree import parse as parse_xml


class QAP_T2438(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.no_related_symbol = [
            {
                "Instrument": {
                    "Symbol": self.eur_gbp,
                    "SecurityType": "self.security_type",
                    "Product": "4",
                },
                "SettlType": self.settle_type_spot,
            }
        ]
        # region SSH
        self.config_file = "client_qf_kharkiv_quod7_th2.xml"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/{self.config_file}"
        # endregion
        self.bands = ["1000000", "3000000"]
        self.tree = None
        self.qs = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare QS configuration
        self.tree = parse_xml(self.local_path)
        self.qs = self.tree.getroot().find("connectivity/adminFeed")
        self.qs.text = 'false'
        self.tree.write("temp.xml", encoding="ISO-8859-1")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QS_ESP_FIX_TH2")
        time.sleep(65)
        # endregion
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbol)
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 2
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands)
        self.md_snapshot.remove_parameters(["OrigMDTime", "OrigMDArrivalTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"],
                                            ignored_fields=["CachedUpdate", "trailer", "header"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager.send_message(self.md_request)
        self.qs.text = 'true'
        self.tree.write("temp.xml", encoding="ISO-8859-1")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QS_ESP_FIX_TH2")
        time.sleep(65)
