import os
from datetime import datetime
from pathlib import Path

from pkg_resources import resource_filename

from custom.verifier import Verifier
from test_framework.data_sets.constants import GatewaySide, Status
from custom.tenor_settlement_date import spo
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2601(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.esp_t_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.config_file = "client_qf_kharkiv_quod7_th2.xml"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/{self.config_file}"
        self.temp_path = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'th2-script-quod-demo', 'temp')
        self.md_req_id = "EUR/USD:SPO:REG:BNP"
        self.no_md_entries_spot = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1815,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": spo(),
            "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
            "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 2000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 2000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.181,
                "MDEntrySize": 7000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18186,
                "MDEntrySize": 7000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.passed = 0
        self.verifier = Verifier()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region 2
        self.new_order_single.set_default_SOR()
        response = self.fix_manager.send_message_and_receive_response(self.new_order_single)
        order_id = response[-1].get_parameters()['OrderID']
        # endregion
        # region 3
        gateway_side_sell = GatewaySide.Sell
        status = Status.Fill
        self.execution_report.set_params_from_new_order_single(self.new_order_single, gateway_side_sell, status,
                                                               response[-1])
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer",
                                                            "header"])
        # endregion
        result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FIXSELLQUODTH2.log", rf"^.*ClientScenarioID=.*{order_id}.*$")
        if result:
            self.passed += 1
        result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FIXSELLQUODTH2.log", rf"^.*{order_id}.*10014=.*$")
        if result:
            self.passed += 1
        if self.passed == 2:
            result = "ok"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"ClientScenarioID\" tag")
        self.verifier.compare_values("status", "ok", result)
        self.verifier.verify()
