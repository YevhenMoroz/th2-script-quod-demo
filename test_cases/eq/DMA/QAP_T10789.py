import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T10789(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client_by_name("client_3")  # CLIENT3
        self.account = "CLIENT3_SA1"  # With default route=ESCHIX
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_3_venue_1")  # XPAR_CLIENT3
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR

        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)

        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(
            self.ssh_client_env.host,
            self.ssh_client_env.port,
            self.ssh_client_env.user,
            self.ssh_client_env.password,
            self.ssh_client_env.su_user,
            self.ssh_client_env.su_password,
        )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Set nativeroute = N for the PARIS venue in RouteVenue table
        self.db_manager.execute_query(
            "UPDATE routevenue SET nativeroute = 'N' WHERE venueid = 'PARIS' AND routeid IN (30, 24);"
        )
        self.ssh_client.send_command("qrestart AQS ORS")
        time.sleep(60)
        # endregion

        # region Step 1-2 Create DMA order
        self.nos.set_default_dma_limit()
        self.nos.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "ClientAccountGroupID": self.client,
                "PreTradeAllocationBlock": {
                    "PreTradeAllocationList": {
                        "PreTradeAllocAccountBlock": [{"AllocClientAccountID": self.account, "AllocQty": self.qty}]
                    }
                },
            },
        )
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(self.price)
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.nos)
            print_message("Create DMA", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Step 2 - Check Route
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {"RouteID": "1", "TransOriginator": "ESCHIX"}, order_reply, "Step 2 - Checking Route"
        )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(
            "UPDATE routevenue SET nativeroute = 'Y' WHERE routeid = 24 AND venueid = 'PARIS';"
        )
        self.ssh_client.send_command("qrestart AQS ORS")
        time.sleep(60)
        self.db_manager.close_connection()
        self.ssh_client.close()

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
