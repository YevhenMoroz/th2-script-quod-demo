import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    ExecutionReportConst,
    JavaApiFields,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T9317(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create DMA order
        self.order_submit.set_default_dma_limit(with_external_algo=True)
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create DMA order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_dma: str = order_reply["OrdID"]
        cl_ord_id: str = order_reply["ClOrdID"]
        # endregion

        # region Precondition - Execute DMA order and checking status
        qty_of_exec = "50"
        self.execution_report.set_default_trade(ord_id_dma)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock", {"LastTradedQty": qty_of_exec, "LeavesQty": qty_of_exec, "CumQty": qty_of_exec}
        )
        responses = self.java_api_manager.send_message_and_receive_response(
            self.execution_report, {ord_id_dma: ord_id_dma}
        )
        print_message("Execution of DMA order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id: str = execution_report_message["ExecID"]  # get ExecID (EX)

        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
                JavaApiFields.ExecPrice.value: str(float(self.price)),
            },
            execution_report_message,
            "Precondition - Checking Status, Price of DMA order after execution",
        )
        # endregion

        # region Step 2 - Modify Man Exec
        price_of_exec_new = "5"
        self.trade_request.get_parameters().clear()
        self.trade_request.set_default_replace_execution(ord_id_dma, exec_id, price_of_exec_new, qty_of_exec)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("Modify Man Exec", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value
        )
        # endregion

        # region Check values
        self.java_api_manager.compare_values(
            {
                JavaApiFields.ExecPrice.value: str(float(price_of_exec_new)),
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
            },
            exec_report,
            "Step 5 - Checking the execution Price after a modification",
        )

        trade_notif = self.java_api_manager.get_last_message(ORSMessageType.TradeEntryNotif.value).get_parameter(
            "TradeEntryNotifBlock"
        )
        self.java_api_manager.compare_values(
            {
                JavaApiFields.ExecPrice.value: str(float(price_of_exec_new)),
                "TradeEntryTransType": "REP",
            },
            trade_notif,
            "Step 5 - Checking the execution Price after a modification",
        )

        list_of_ignored_fields: list = ["ExecID", "GatingRuleCondName", "OrderQtyData", "NoStrategyParameters",
                                        "LastQty", "GatingRuleName", "TransactTime", "Side", "QuodTradeQualifier",
                                        "BookID", "SettlCurrency", "SettlDate", "Currency", "TimeInForce",
                                        "PositionEffect", "TradeDate", "HandlInst", "LeavesQty", "NoParty", "CumQty",
                                        "OrdType", "SecondaryOrderID", "tag5120", "LastMkt", "OrderCapacity", "QtyType",
                                        "ExecBroker", "StrategyName", "Price", "VenueType", "Instrument",
                                        "ExDestination", "GrossTradeAmt"]
        self.exec_report.change_parameters(
            {
                "ExecType": "G",
                "OrdStatus": "1",
                "OrderID": ord_id_dma,
                "ClOrdID": cl_ord_id,
                "Account": self.client,
                "AvgPx": price_of_exec_new,
                "LastPx": price_of_exec_new,
                "ExecRefID": exec_id,
            }
        )
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.exec_report, ["OrderID", "OrdStatus", "ExecType"], ignored_fields=list_of_ignored_fields
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
