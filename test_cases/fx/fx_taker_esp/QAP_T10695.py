from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T10695(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.env = self.environment.get_list_fix_environment()[0]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.env.feed_handler, self.test_id)
        self.fix_verifier = FixVerifier(self.env.drop_copy, self.test_id)
        self.fix_manager_gtw = FixManager(self.env.buy_side_esp, self.test_id)
        self.side = GatewaySide.Sell
        self.status = Status.Fill
        self.new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report_filled_1 = FixMessageExecutionReportAlgoFX()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.result = str()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.fix_md.set_market_data().update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md)
        md_req_id = self.fix_md.get_parameters()["MDReqID"]
        last_update_time = self.fix_md.get_parameters()["LastUpdateTime"]
        # region Step 1
        self.new_order_sor.set_default_SOR()
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        order_id = response[-1].get_parameters()['OrderID']
        # endregion
        # region Step 2
        self.execution_report_filled_1. \
            set_params_from_new_order_single(self.new_order_sor, self.side, self.status, response=response[-1])
        self.execution_report_filled_1.change_parameter("LastQty", "*")
        self.execution_report_filled_1.update_repeating_group("NoStrategyParameters", "*")
        self.execution_report_filled_1.remove_parameter("OrderCapacity")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report_filled_1,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName",
                                                            "trailer", "header"])
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FXFH.log",
                                                         rf"^.*{md_req_id}.*QuoteLastUpdateTime =.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "failed"
        print(self.result)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"QuoteLastUpdateTime\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FXFH.log",
                                                         rf"^.*{md_req_id}.*10779={last_update_time}.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "failed"
        print(self.result)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"10779\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.FIXBUYTH2ESPO.log",
                                                         rf"^.*35=D.*10779={last_update_time}.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "failed"
        print(self.result)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"10779\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        # endregion
