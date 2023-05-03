import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7139(TestCase):
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
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price)
            )
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters({"Side": "2", "OrderQtyData": {"OrderQty": self.qty}})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Order ID
            order_id = response[0].get_parameters()["OrderID"]

        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Step 2 - Check ExecutionReports, 2376=1011
        party_stub_dict = {"PartyRole": "*", "PartyRoleQualifier": "*", "PartyID": "*", "PartyIDSource": "*"}
        parties = {
            "NoPartyIDs": [
                party_stub_dict,
                party_stub_dict,
                party_stub_dict,
                {"PartyRole": "*", "PartyRoleQualifier": "1011", "PartyID": "*", "PartyIDSource": "*"},
            ]
        }

        list_of_ignored_fields: list = ["ReplyReceivedTime", "SecondaryOrderID", "Text", "LastMkt",
                                        "GatingRuleCondName", "GatingRuleName"]
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters({"Parties": parties})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_of_ignored_fields)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
