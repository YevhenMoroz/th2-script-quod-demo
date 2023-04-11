import logging
from datetime import datetime
from pathlib import Path

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7108(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '7108'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_mic = self.data_set.get_mic_by_name('mic_1')
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create DMA  step 1
        self.order_submit.set_default_dma_limit()
        route = self.data_set.get_route_id_by_name("route_1")
        route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: route}]}
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.RouteList.value: route_params,
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.Price.value: self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             order_reply, 'Verifying that order created (step 1)')
        # endregion

        # region step 2: Partially Filled DMA order
        self.execution_report.set_default_trade(order_id)
        half_qty = int(int(self.qty) / 2)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             JavaApiFields.Side.value: "Buy",
                                                             JavaApiFields.LastTradedQty.value: half_qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: "Limit",
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.ExecType.value: "Trade",
                                                             JavaApiFields.TimeInForce.value: "Day",
                                                             JavaApiFields.LeavesQty.value: half_qty,
                                                             JavaApiFields.CumQty.value: half_qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, actually_result,
            'Compare actually and expected result from step 2')
        # endregion

        # region step 3 : Fully Fill DMA order
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.LeavesQty.value: '0',
            JavaApiFields.VenueExecID.value: bca.client_orderid(9),
        })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            'Compare actually and expected result Execution from step 3')
        # endregion

        # region step 4-5-6: Book DMA order
        self.allocation_instruction.set_default_book(order_id)
        trade_date_new = (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y-%m-%dT%H:%M:%S')
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.Qty.value: self.qty,
                                                                   JavaApiFields.AccountGroupID.value: self.client,
                                                                   JavaApiFields.TradeDate.value: trade_date_new
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        trade_date_actually = allocation_report[JavaApiFields.TradeDate.value][:10]
        self.java_api_manager.compare_values({JavaApiFields.TradeDate.value: trade_date_new[:10]},
                                             {JavaApiFields.TradeDate.value: trade_date_actually},
                                             'Verify that block has properly trade date (step 6)')
        # endregion

        # region step 7: Approve and Allocate block
        # part 1: Approve block
        self.approve_block.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.approve_block)
        # end_of_part

        # part 2: Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            JavaApiFields.AllocAccountID.value: self.alloc_account,
            JavaApiFields.AllocQty.value: self.qty,
            JavaApiFields.TradeDate.value: trade_date_new})
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report, 'Verify that block has properly statuses after allocation (step 7)')

        self.java_api_manager.compare_values(
            {JavaApiFields.AffirmStatus.value: ConfirmationReportConst.AffirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value},
            confirmation_report, 'Verifying that allocation has properly statuses (step 7)')
        # end_of_part
        # endregion

        # region part 8: Check that 35 = AK message has properly value for Allocation
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        list_of_ignored_fields = ['ConfirmType', 'MatchStatus', 'ConfirmStatus',
                                  'CpctyConfGrp', 'ConfirmID', 'ConfirmTransType',
                                  'AllocQty', 'AllocAccount', 'AvgPx',
                                  'TransactTime', 'Side', 'IndividualAllocID',
                                  'BookID', 'SettlDate', 'AllocID',
                                  'Currency', 'NetMoney', 'NoParty', 'ReportedPx',
                                  'Instrument', 'GrossTradeAmt','OrderAvgPx'
                                  ]
        confirmation_report.change_parameters({'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': order_id,
        }], 'TradeDate': str(trade_date_new[:10]).replace('-', '')})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report, ['ClOrdID', 'AllocAccount'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion
