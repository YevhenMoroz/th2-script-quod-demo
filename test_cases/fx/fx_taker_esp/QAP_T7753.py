from copy import deepcopy
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import GatewaySide
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiListingCounterpartMessages import RestApiListingCounterpartMessages
from test_framework.rest_api_wrappers.forex.RestApiVenueMessages import RestApiVenueMessages
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T7753(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.env.drop_copy, self.test_id)
        self.fix_manager_gtw = FixManager(self.env.buy_side_esp, self.test_id)
        self.venue_message = RestApiVenueMessages()
        self.side = GatewaySide.Sell
        self.new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report_filled_1 = FixMessageExecutionReportAlgoFX()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.result = str()
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.listing_counterpart = RestApiListingCounterpartMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.listing_counterpart_record = [{"counterpartID": 1000010, "partyRole": "CLI"}]
        self.hsbc_sw = self.data_set.get_market_id_by_name("market_2")
        self.log_path = "/Logs/quod314/QUOD.FIXBUYTH2ESPO.log"
        self.msg_prams_client = None
        self.msg_prams_client_default = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.listing_counterpart.set_default_params().manage_listing_counterpart(self.listing_counterpart_record)
        self.rest_manager.send_post_request(self.listing_counterpart)
        self.sleep(4)
        # region Step 1
        self.new_order_sor.set_default_mo().change_parameter("ExDestination", self.hsbc_sw)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        order_id = response[-1].get_parameters()['OrderID']
        # endregion
        # region Step 2
        self.result = self.ssh_client.find_regex_pattern(
            self.log_path,
            rf"^.*gateway NewOrderSingle.*PartyID=.TESTCP_ClinetID..PartyIDSource=Proprietary.PartyRole=ClientID.*{order_id}.*$")
        if self.result:
            self.result = "passed"
        else:
            self.result = "failed"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check PartiesBlock")
        self.verifier.compare_values("status", "passed", self.result)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.listing_counterpart.set_default_params()
        self.rest_manager.send_post_request(self.listing_counterpart)
        self.sleep(2)
