import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7076(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.instrument_1 = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.mic_blm = self.data_set.get_mic_by_name('mic_1_blm')  # XPAR_BLM
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
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "A"}, exec_rep, "Check Status")
        self.fix_message.update_fields_in_component("Instrument", {"SecurityExchange": self.mic})
        self.fix_manager.compare_values(self.instrument_1, exec_rep["Instrument"], "Check instrument")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.send_command("sql")
        self.ssh_client.send_command(f"UPDATE exchangecode SET bloombergexchcode=null WHERE mic='{self.mic}';")
        self.ssh_client.send_command("exit")
        self.ssh_client.send_command("qrestart AQS ORS ESBUYTH2TEST")
        time.sleep(70)
