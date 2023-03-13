import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7240(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message1.get_parameter("Price")
        self.qty = self.fix_message1.get_parameter("OrderQtyData")["OrderQty"]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.manual_cross = ManualOrderCrossRequest()
        self.fix_verifier_sell = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.exec_price = "30"
        self.exec_qty1 = "100"
        self.exec_qty2 = "80"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        # Create 1 Care order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message1)
        order_id1 = response[0].get_parameter("OrderID")

        # Create 2 Care order
        self.fix_message2.change_parameters({"Side": "2"})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message2)
        order_id2 = response[0].get_parameter("OrderID")

        # Manual cross them
        self.manual_cross.set_default(self.data_set, order_id1, order_id2, self.exec_price, self.exec_qty1)
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        # endregion

        # region Check ExecSts
        exp_res = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}
        exec_report_1 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id1
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_1, "Checking ExecSts of the 1 order")
        exec_report_2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id2
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_2, "Checking ExecSts of the 2 order")
        # endregion

        # region Step 1 - Extract ManualOrderCrossID
        man_order_cross_id = self.java_api_manager.get_last_message(
            ORSMessageType.ManualOrderCrossReply.value
        ).get_parameter(JavaApiFields.ManualOrderCrossReplyBlock.value)["ManualOrderCrossID"]
        # endregion

        # region Step 2-4 - Modify Man Cross
        self.manual_cross.update_fields_in_component(
            "ManualOrderCrossRequestBlock",
            {
                "ExecQty": self.exec_qty2,
                "ManualOrderCrossTransType": "Replace",
                "ManualOrderCrossID": man_order_cross_id,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        # endregion

        # region Check ExecSts
        exp_res = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}
        exec_report_1 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id1
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_1, "Step 4 - Checking ExecSts of the 1 order")
        exec_report_2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id2
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_2, "Step 4 - Checking ExecSts of the 2 order")
        # endregion

        # region Step 5 - Check Execution reports in BO
        ignored_fields: list = [
            "GatingRuleCondName",
            "ExecRefID",
            "GatingRuleName",
            "TrdSubType",
            "SettlCurrency",
            "LastExecutionPolicy",
            "TrdType",
            "SecondaryOrderID",
            "LastMkt",
            "VenueType",
            "SecondaryExecID",
            "LastCapacity", "Parties", "QuodTradeQualifier", "BookID", "TradeReportingIndicator", "NoParty", "tag5120",
            "ExecBroker"
        ]
        self.exec_report.set_default_filled(self.fix_message1)
        self.exec_report.change_parameters({"ExecType": "G", "OrdStatus": "1"})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ["Side", "OrdStatus", "ExecType"], ignored_fields=ignored_fields
        )

        self.exec_report.set_default_filled(self.fix_message2)
        self.exec_report.change_parameters({"ExecType": "G", "OrdStatus": "1"})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ["Side", "OrdStatus", "ExecType"], ignored_fields=ignored_fields
        )
        # endregion

        # region Step 6,7 - Cancel Man Cross
        self.manual_cross.update_fields_in_component(
            "ManualOrderCrossRequestBlock",
            {"ManualOrderCrossTransType": "Cancel", "ManualOrderCrossID": man_order_cross_id},
        )
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        # endregion

        # region Checking that Man Сross is canceled
        exp_res = {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value}
        exec_report_1 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id1
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_1, "Step 7 - Check execution of 1 order")
        exec_report_2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id2
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(exp_res, exec_report_2, "Step 7 - Check execution of 2 order")
        # endregion

        # region Step 8  - Check Execution reports in BO
        self.exec_report.set_default_trade_cancel(self.fix_message1)
        self.exec_report.change_parameters({"ExecType": "H"})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ["Side", "OrdStatus", "ExecType"], ignored_fields=ignored_fields
        )
        self.exec_report.set_default_trade_cancel(self.fix_message2)
        self.exec_report.change_parameters({"ExecType": "H"})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ["Side", "OrdStatus", "ExecType"], ignored_fields=ignored_fields
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
