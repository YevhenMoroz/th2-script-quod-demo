import logging
import time
from copy import deepcopy
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from datetime import datetime
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, \
    OrderReplyConst, AllocationReportConst, OrdTypes, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7000(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_verifier_buy_side = FixVerifier(self.bs_connectivity, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.fix_modification = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.rest_institution_message = RestApiModifyInstitutionMessage(self.data_set)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.qty = '300'
        self.price = '10'

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set needed values via WebAdmin
        self.rest_institution_message.modify_enable_unknown_accounts(True)
        self.rest_api_manager.send_post_request(self.rest_institution_message)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(45)
        # endregion

        # region step 1: create DMA  order
        # part 1: Create DMA order
        dummy_account = 'GVNCH'
        currency_USD = self.data_set.get_currency_by_name('currency_4')
        self.new_order_single.set_default_dma_limit()
        cl_ord_id = self.new_order_single.get_parameter('ClOrdID')
        pre_alloc_grp = {"PreAllocGrp": {"NoAllocs": [
            {"AllocAccount": dummy_account, "AllocQty": self.qty,
             'AllocSettlCurrency': currency_USD}]}}
        self.new_order_single.change_parameters({
            "Price": self.price,
            "Account": self.client,
            "Side": "1",
            'OrderQtyData': {'OrderQty': self.qty},
            "PreAllocGrp": pre_alloc_grp['PreAllocGrp']})
        self.fix_manager.send_message_fix_standard(self.new_order_single)
        time.sleep(5)
        order_id = self.db_manager.execute_query(f"SELECT ordid FROM ordr WHERE clordid = '{cl_ord_id}'")[
            0][0]
        self.execution_report.set_default_new(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.LeavesQty.value: self.qty,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id})
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
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
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'OrderAvgPx',
                                  'tag11245', 'ExecAllocGrp', 'SettlCurrFxRate', 'ConfirmType', 'SettlCurrFxRateCalc',
                                  'MatchStatus', 'ConfirmStatus', 'SettlCurrAmt', 'CpctyConfGrp', 'ConfirmTransType',
                                  'SettlCurrency', 'AllocSettlCurrAmt', 'TradeReportingIndicator', 'OrigClOrdID',
                                  'SettlType'
                                  ]
        fix_new_order_single_check = deepcopy(self.new_order_single)
        fix_new_order_single_check.change_parameters({'ClOrdID': order_id})
        fix_new_order_single_check.change_parameters({
            'PreAllocGrp': {'NoAllocs':
                [{
                    'AllocSettlCurrency': currency_USD,
                    'AllocQty': self.qty,
                    'AllocAccount': dummy_account
                }]}})
        self.fix_verifier_buy_side.check_fix_message_fix_standard(fix_new_order_single_check,
                                                                  key_parameters=['ClOrdID'],
                                                                  ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

        # region step 2: Modify DMA order
        # part 1: Send modification request and send reply
        new_qty = '500'
        self.fix_modification.set_default(self.new_order_single, qty=new_qty)
        self.fix_modification.change_parameters(pre_alloc_grp)
        self.fix_modification.get_parameter('PreAllocGrp')['NoAllocs'][0]['AllocQty'] = new_qty
        self.fix_manager.send_message_fix_standard(self.fix_modification)
        time.sleep(3)
        ord_modify_id = self.db_manager.execute_query(f"SELECT ordmodifyid FROM ordmodify WHERE ordid = '{order_id}'")[
            0][0]
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_Replaced.value,
                                                             JavaApiFields.LeavesQty.value: new_qty,
                                                             JavaApiFields.ClOrdID.value: ord_modify_id,
                                                             JavaApiFields.OrdQty.value: new_qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id})
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
             JavaApiFields.OrdQty.value: str(float(new_qty))},
            ord_reply, 'Verifying that order has properly values (step 2)')
        # end_of_part

        # part 2 : Check 35 = G message on Buy GateWay
        self.fix_modification.get_parameters()['ClOrdID'] = ord_modify_id
        self.fix_modification.remove_parameter('PreAllocGrp')
        self.fix_modification.get_parameters()['PreAllocGrp'] = pre_alloc_grp['PreAllocGrp']
        self.fix_verifier_buy_side.check_fix_message_fix_standard(self.fix_modification, ['ClOrdID'],
                                                                  ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

        # region step 3: Fully Fill DMA order
        # part 1: Fill DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.Side.value: SubmitRequestConst.Side_Buy.value,
                                                             JavaApiFields.LastTradedQty.value: new_qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                                                             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_Trade.value,
                                                             JavaApiFields.CumQty.value: new_qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: new_qty
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
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_filled(self.new_order_single)
        execution_report.get_parameters()['M_PreAllocGrp'] = pre_alloc_grp['PreAllocGrp']
        execution_report.get_parameter('M_PreAllocGrp')['NoAllocs'][0]['AllocQty'] = new_qty
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

        # region step 4: Book DMA order
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_2')
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.Qty.value: new_qty,
                                                                   JavaApiFields.AccountGroupID.value: self.client,
                                                                   JavaApiFields.InstrID.value: instrument_id
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

        # region step 5: Approve and Allocate block
        # part 1 : Approve Block
        self.approve_block.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_block)
        # end_of_part

        # part 2 : Allocate Block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.remove_fields_from_component(JavaApiFields.ConfirmationBlock.value,
                                                               [JavaApiFields.AllocAccountID.value])
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value,
                                                             {JavaApiFields.AllocQty.value: new_qty,
                                                              JavaApiFields.AllocFreeAccountID.value: dummy_account,
                                                              JavaApiFields.InstrID.value: instrument_id,
                                                              JavaApiFields.SettlCurrency.value: currency_USD}
                                                             )
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AllocFreeAccountID.value: dummy_account,
                                              JavaApiFields.SettlCurrency.value: currency_USD}, confirmation_report,
                                             'Verify that confirmation has correct values (step 5)')
        # end_of_part
        # endregion

        # region step 6: Check 35 = AK and 35 = J message
        # part 1: Check 35 = J message
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_preliminary(self.new_order_single)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        # end_of_part

        # part 2 check 35 = AK message
        list_of_ignored_fields.remove('SettlCurrency')
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_report.set_default_confirmation_new(self.new_order_single)
        confirmation_report.change_parameters({'SettlCurrency': currency_USD,
                                               'AllocQty': new_qty})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                         ['AllocAccount', 'NoOrders'],
                                                         ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_institution_message.modify_enable_unknown_accounts(False)
        self.rest_api_manager.send_post_request(self.rest_institution_message)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(45)
