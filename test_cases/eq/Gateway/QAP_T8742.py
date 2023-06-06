import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from datetime import datetime
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, \
    OrderReplyConst, AllocationReportConst, OrdTypes, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T8742(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_verifier_buy_side = FixVerifier(self.bs_connectivity, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.qty = '300'
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create DMA  order
        # part 1: Create DMA order
        dummy_account = 'GVNCH'
        currency_USD = self.data_set.get_currency_by_name('currency_4')
        self.submit_request.set_default_dma_limit()
        route_params = {JavaApiFields.RouteBlock.value: [
            {JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.RouteList.value: route_params,
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.PreTradeAllocationBlock.value: {
                JavaApiFields.PreTradeAllocationList.value: {JavaApiFields.PreTradeAllocAccountBlock.value: [
                    {JavaApiFields.AllocFreeAccountID.value: dummy_account,
                     JavaApiFields.AllocQty.value: self.qty,
                     JavaApiFields.AllocSettlCurrency.value: currency_USD}]}},
            JavaApiFields.Price.value: self.price
        })
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_reply[JavaApiFields.OrdID.value]
        cl_ord_id = ord_reply[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
             JavaApiFields.OrdQty.value: str(float(self.qty))},
            ord_reply,
            'Verifying expected and actually result (step 1)')
        self.java_api_manager.compare_values({JavaApiFields.AllocFreeAccountID.value: dummy_account,
                                              JavaApiFields.AllocQty.value: str(float(self.qty)),
                                              JavaApiFields.AllocSettlCurrency.value: currency_USD},
                                             ord_reply[JavaApiFields.PreTradeAllocationBlock.value][
                                                 JavaApiFields.PreTradeAllocationList.value][
                                                 JavaApiFields.PreTradeAllocAccountBlock.value][0],
                                             'Verify that Order has properly AllocAccount and AllocQty (step 1)')
        # end_of_part

        # part 2: Verify 35=D message on BuySide
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'MaxPriceLevels', 'Parties',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocQty', 'AllocPrice', 'OrderAvgPx',
                                  'tag11245', 'ExecAllocGrp',
                                  'SettlCurrFxRate', 'SettlCurrFxRateCalc', 'MatchStatus', 'ConfirmType',
                                  'ConfirmID', 'ConfirmTransType', 'CpctyConfGrp', 'SettlCurrAmt', 'ConfirmStatus',
                                  'AllocSettlCurrAmt']
        fix_new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        change_parameters = {
            'ClOrdID': order_id,
            'TransactTime': '*',
            'SettlCurrency': '*',
            'PreAllocGrp': {'NoAllocs':
                [{
                    'AllocSettlCurrency': currency_USD,
                    'AllocQty': self.qty,
                    'AllocAccount': dummy_account
                }]}
        }
        fix_new_order_single.change_parameters(change_parameters)
        self.fix_verifier_buy_side.check_fix_message_fix_standard(fix_new_order_single, key_parameters=['ClOrdID'],
                                                                  ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

        # region step 2: Fully Fill DMA order
        # part 1: Fill DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.Side.value: SubmitRequestConst.Side_Buy.value,
                                                             JavaApiFields.LastTradedQty.value: self.qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_Trade.value,
                                                             JavaApiFields.LeavesQty.value: '0',
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            'Verifying that order fully filled (step 2)')

        # part 2: Check 35=8 (39=2) message for BackOffice
        change_parameters['ClOrdID'] = cl_ord_id
        change_parameters['M_PreAllocGrp'] = change_parameters.pop('PreAllocGrp')
        execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        execution_report.change_parameters({'ExecType': 'F', "OrdStatus": "2"})
        list_of_ignored_fields.append('PreAllocGrp')
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        list_of_ignored_fields.remove('PreAllocGrp')
        # end_of_part
        # endregion

        # region step 3: Book DMA order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.Qty.value: self.qty,
                                                                   JavaApiFields.AccountGroupID.value: self.client,
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_update, 'Verifying that order Booked (step 3)')
        # endregion

        # region step 4: Approve block
        self.approve_block.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_block)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value}, allocation_report,
            'Verifying that block has properly statuses (step 4)')
        # endregion

        # region step 5-6: Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.remove_fields_from_component(JavaApiFields.ConfirmationBlock.value,
                                                               [JavaApiFields.AllocAccountID.value])
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value,
                                                             {JavaApiFields.AllocQty.value: self.qty,
                                                              JavaApiFields.AllocFreeAccountID.value: dummy_account,
                                                              JavaApiFields.SettlCurrency.value: currency_USD}
                                                             )
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AllocFreeAccountID.value: dummy_account,
                                              JavaApiFields.SettlCurrency.value: currency_USD}, confirmation_report,
                                             'Verify that confirmation has correct values (step 6)')
        # endregion

        # region step 7: Check 35 = AK and 35 = J message
        # part 1: Check 35 = J message
        change_parameters.clear()
        change_parameters = {
            'AllocType': 2,
            'NoOrders': [{
                'ClOrdID': cl_ord_id,
                'OrderID': order_id
            }],
            'NoAllocs': [{
                'AllocSettlCurrency': currency_USD,
                'SettlCurrency': currency_USD,
                'AllocAccount': dummy_account
            }]}
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        # end_of_part

        # part 2 check 35 = AK message
        del change_parameters['AllocType']
        del change_parameters['NoAllocs']
        change_parameters['SettlCurrency'] = currency_USD
        change_parameters['AllocAccount'] = dummy_account
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                         ['AllocAccount', 'NoOrders'],
                                                         ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion
