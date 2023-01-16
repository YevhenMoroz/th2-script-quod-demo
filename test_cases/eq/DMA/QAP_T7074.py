import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7074(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.mic_blm = self.data_set.get_mic_by_name('mic_1_blm')  # XPAR_BLM
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.ssh_client.send_command("sql")
        self.ssh_client.send_command(
            f"UPDATE exchangecode SET bloombergexchcode='{self.mic_blm}' WHERE mic='{self.mic}';")
        self.ssh_client.send_command("exit")
        self.ssh_client.send_command("qrestart AQS ORS ESBUYTH2TEST")
        time.sleep(70)
        # endregion
        self.fix_message.remove_parameter("ExDestination")
        self.fix_message.update_fields_in_component("Instrument", {"SecurityExchange": self.mic_blm})
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        ord_id = response[0].get_parameter("OrderID")
        self.fix_message.change_parameters(
            {"Account": venue_client_account, "ClOrdID": ord_id, "ExDestination": self.mic})
        self.fix_message.remove_fields_from_component("Instrument", ["SecurityDesc"])
        ignored_fields = ["TransactTime", "Parties", "SettlDate"]
        self.fix_verifier.check_fix_message_fix_standard(self.fix_message, ["ClOrdID"], ignored_fields=ignored_fields)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.send_command("sql")
        self.ssh_client.send_command(f"UPDATE exchangecode SET bloombergexchcode=null WHERE mic='{self.mic}';")
        self.ssh_client.send_command("exit")
        self.ssh_client.send_command("qrestart AQS ORS ESBUYTH2TEST")
        time.sleep(70)
