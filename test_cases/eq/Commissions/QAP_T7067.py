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
from test_framework.data_sets.oms_data_set.oms_const_enum import OMSFee
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7067(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission and fees
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_fees_message(comm_profile=self.perc_amt, fee=OMSFee.fee1)
        self.commission_sender.change_message_params({"venueListID": 1})
        self.commission_sender.send_post_request()
        time.sleep(2)
        # endregion

        # region Step 1 - Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )
            self.submit_request.set_default_dma_limit()
            self.submit_request.update_fields_in_component(
                "NewOrderSingleBlock",
                {
                    "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                    "AccountGroupID": self.client,
                    "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
                },
            )
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Step 2 - Execute CO and check fee
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        expected_result = {
            JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
            "ExecCommission": "1.0",
        }
        self.java_api_manager.compare_values(expected_result, exec_reply, "Compare TransExecStatus and ExecCommission")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
