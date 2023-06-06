import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    ConfirmationReportConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7464(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.rest_api_manager = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        indicators_list = [self.data_set.get_net_gross_ind_type('gross_ind'),
                           self.data_set.get_net_gross_ind_type('net_ind')]
        # endregion
        for indicator in indicators_list:
            # region create and execute dma order

            # part 1 : Create DMA order
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component(
                "NewOrderSingleBlock",
                {"OrdQty": qty,
                 "AccountGroupID": self.client,
                 "Price": price,
                 "ClOrdID": bca.client_orderid(9)})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            ord_id = order_reply[JavaApiFields.OrdID.value]
            # end of part

            # part 2 (trade dma order)
            self.execution_report.set_default_trade(ord_id)
            self.execution_report.update_fields_in_component(
                "ExecutionReportBlock",
                {
                    "Price": price,
                    "AvgPrice": price,
                    "LastPx": price,
                    "OrdQty": qty,
                    "LastTradedQty": qty,
                    "CumQty": qty,
                    "VenueExecID": bca.client_orderid(9),
                    "LastVenueOrdID": bca.client_orderid(12)
                },
            )
            self.java_api_manager.send_message_and_receive_response(self.execution_report)
            execution_report_message = self.java_api_manager.get_last_message(
                ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
            ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value, },
                execution_report_message,
                f"Comparing ExecSts after Execute DMA ({indicator}))")
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value, },
                order_reply,
                "Comparing PostTradeStatus after Execute DMA ", )
            exec_id = execution_report_message[JavaApiFields.ExecID.value]
            # end of part

            # endregion

            # region  Book order
            self.allocation_instruction.set_default_book(ord_id)
            gross_trade_amt = float(price) * float(qty)
            self.allocation_instruction.set_default_book(ord_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                                   {"Qty": qty,
                                                                    "AvgPx": price,
                                                                    'GrossTradeAmt': str(gross_trade_amt),
                                                                    "SettlCurrAmt": str(gross_trade_amt),
                                                                    'ExecAllocList': {
                                                                        'ExecAllocBlock': [{'ExecQty': qty,
                                                                                            'ExecID': exec_id,
                                                                                            'ExecPrice': price}]},
                                                                    'NetGrossInd': indicator
                                                                    })
            self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
                allocation_report,
                f'Check expected and actually results for block ({indicator})')
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
                order_update, f'Check expected and actually result for order ({indicator})')
            self.approve_message.set_default_approve(alloc_id)
            self.java_api_manager.send_message_and_receive_response(self.approve_message)
            # endregion

            # region  Allocate block
            self.confirmation_request.set_default_allocation(alloc_id)
            self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                                 {"AllocQty": qty,
                                                                  "Side": "B",
                                                                  "AvgPx": price,
                                                                  "AllocAccountID": self.alloc_account})
            self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            confirmation_id = confirmation_report[JavaApiFields.ConfirmationID.value]
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                 JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
                allocation_report,
                f'Check expected and actually results for block ({indicator})')
            self.java_api_manager.compare_values({
                JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value
            }, confirmation_report, f'Check expected and actually results for allocation ({indicator})')
            # endregion

            # region Check Fix_Confirmation message in ors logs
            self.ssh_client.send_command('cdl')
            self.ssh_client.send_command('egrep "serializing fix Confirmation={.*. } }" QUOD.ORS.log > logs.txt')
            self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
            self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
            with open('./logs.txt') as file:
                res = file.read()
                self.java_api_manager.compare_values({
                    "ConfirmationID": f"ConfirmationID={confirmation_id}", "NetGrossInd": f"NetGrossInd={indicator}"}, {
                    "ConfirmationID": res, "NetGrossInd": res}, "Check ORS message",
                    VerificationMethod.CONTAINS)
            os.remove('./logs.txt')
            # endregion
