import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationReportConst, OrderReplyConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7360(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "200"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_4")  # MOClient4 CS = Manual, AP = Auto, Other Manual
        self.alloc_account_1 = self.data_set.get_account_by_name("client_pt_4_acc_1")  # MOClient4_SA1
        self.alloc_account_2 = self.data_set.get_account_by_name("client_pt_4_acc_2")  # MOClient4_SA2
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step  1 : Create DMA order
        self.order_submit.set_default_dma_limit()
        half_qty = str(float(self.qty) / 2)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty,
             "AccountGroupID": self.client,
             "Price": self.price,
             "PreTradeAllocationBlock": {
                 "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                     {"AllocAccountID": self.alloc_account_1, "AllocQty": half_qty},
                     {"AllocAccountID": self.alloc_account_2, "AllocQty": half_qty}
                 ]}}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # endregion

        # region step 2 (trade dma order)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # self.java_api_manager.compare_values({JavaApiFields.TransStatus.value:ExecutionReportConst.})
        # endregion

        # part 3 book order
        self.allocation_instruction.set_default_book(ord_id)
        gross_trade_amt = float(self.price) * float(self.qty)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": self.qty,
                                                                "AvgPx": self.price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                'AccountGroupID': self.client,
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': self.price}]},
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value},
            allocation_report,
            f'Check expected and actually results for block (step 3)')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, f'Check expected and actually result for order (step 3)')
        # end of part

        # endregion

        # region step 4 : Approve block
        list_of_allocations = [self.alloc_account_1, self.alloc_account_2]
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value},
            allocation_report,
            f'Check expected and actually results for block (step 4)')
        for account in list_of_allocations:
            confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value,
                                                                         f"'{account}'").get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
            self.java_api_manager.compare_values({
                JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value
            }, confirmation_report, f'Check expected and actually results for allocation with {account} (step 4)')
        # endregion

        # region step 5 : Check Fix_Confirmation
        for account in list_of_allocations:
            list_of_ignored_fields = ['AllocQty', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                                      'BookID', 'SettlDate', 'OrderAvgPx', 'Currency',
                                      'NetMoney', 'MatchStatus', 'ConfirmStatus', 'TradeDate',
                                      'NoParty', 'AllocInstructionMiscBlock1', 'tag5120',
                                      'ReportedPx', 'Instrument', 'GrossTradeAmt']
            list_of_ignored_fields.extend(['CpctyConfGrp', 'ConfirmID', 'ConfirmType'])
            self.confirmation_message.change_parameters(
                {'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': ord_id}],
                 'ConfirmTransType': "0",
                 'Account': '#',
                 'AllocID': alloc_id,
                 'AllocAccount': account})
            self.fix_verifier_dc.check_fix_message_fix_standard(self.confirmation_message,
                                                                ['ConfirmTransType', 'NoOrders', 'AllocAccount'],
                                                                ignored_fields=list_of_ignored_fields)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
