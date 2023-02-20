import logging
import time
from datetime import datetime, timedelta
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


class QAP_T7614(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "500"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.future_date = datetime.now() + timedelta(days=4)
        self.expire_date = datetime.strftime(self.future_date, "%Y%m%d")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, True, 0, 0
            )
            self.fix_message.set_default_dma_market()
            self.fix_message.change_parameters(
                {
                    "Side": "2",
                    "OrderQtyData": {"OrderQty": self.qty},
                    "TimeInForce": "6",
                    "ExpireDate": self.expire_date,
                }
            )
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID
            cl_ord_id = response[0].get_parameters()["ClOrdID"]

        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Set-up parameters for ExecutionReports
        list_of_ignored_fields: list = [
            "ReplyReceivedTime",
            "SecondaryOrderID",
            "LastMkt",
            "Text",
            "Instrument",
            "Price",
            "SettlDate",
            "OrigClOrdID",
             "GatingRuleCondName",
            "GatingRuleName"
        ]

        # Depends on Weekend Day settings on Venue
        # if self.future_date.isoweekday() == 6:
        #     self.expire_date = datetime.strftime(self.future_date - timedelta(days=1), "%Y%m%d")
        # elif self.future_date.isoweekday() == 7:
        #     self.expire_date = datetime.strftime(self.future_date - timedelta(days=2), "%Y%m%d")

        self.exec_report.set_default_canceled(self.fix_message).change_parameters(
            {"OrdStatus": "4", "CxlQty": self.qty, "ExpireDate": self.expire_date}
        )
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_of_ignored_fields)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
