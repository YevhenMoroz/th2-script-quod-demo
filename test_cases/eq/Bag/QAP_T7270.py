import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, BagChildCreationPolicy, \
    OrderBagConst, OrdTypes
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.fix_wrappers import DataSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7270(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '1000'
        self.price = '5'
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.order_action_request = OrderActionRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')

        # subregion Precondition: Create 1st CO via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price':self.price})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        cl_ord_id1 = response[0].get_parameters()['ClOrdID']
        order_id1 = response[0].get_parameters()['OrderID']

        # subregion Precondition: Create 2nd CO via FIX
        self.fix_message2.set_default_care_limit()
        self.fix_message2.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response2 = self.fix_manager.send_message_and_receive_response(self.fix_message2)
        cl_ord_id2 = response2[0].get_parameters()['ClOrdID']
        order_id2 = response2[0].get_parameters()['OrderID']
        orders_id = [order_id1, order_id2]

        # subregion Precondition: Set DiscloseExec = Manual
        self._set_manual_disclose_exec(order_id1)
        self._set_manual_disclose_exec(order_id2)
        # endregion

        # region Step 1-2-3: Bag Split by AVG
        bag_name = 'QAP_T7270'
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: bag_name,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, 'Step 1-2-3: Verify bag is created')
        # endregion

        # region Step 4-5-6-7: Wave Bag and Partially Fill it
        qty_of_bag = str(int(int(self.qty) * 2))
        trd_qty = '300'
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          venue_client_account,
                                                                                          exec_destination,
                                                                                          int(self.price),
                                                                                          int(trd_qty), 0)
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)

        leavesqty = int(int(self.qty)) * 2 - int(int(trd_qty) * 2)
        cumqty = int(int(trd_qty) * 2)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value).get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           JavaApiFields.LeavesQty.value: str(leavesqty)+'.0',
                           JavaApiFields.CumQty.value: str(cumqty)+'.0'}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Step 4-5-6: Checking Wave status, leavesqty, cumqty")

        bag_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[JavaApiFields.OrderBagNotificationBlock.value]
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           JavaApiFields.OrderBagExecStatus.value: 'PFL'}
        self.java_api_manager.compare_values(expected_result, bag_notify, "Step 4-5-6: Checking Bag is Partially Filled")

        execution_report_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        execution_report_co_order_id = execution_report_co_order["ExecID"]
        # endregion

        # Step 8 - Verify GTW doesn't have 35=8 message with 39=1
        self.fix_verifier.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                pre_filter={
                                                    "OrdStatus": "1",
                                                    "ClOrdID": cl_ord_id1
                                                })
        self.fix_verifier.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                 pre_filter={
                                                     "OrdStatus": "1",
                                                     "ClOrdID": cl_ord_id2
                                                 })
        # endregion

        # Step 9 - Exec Summary
        qty_to_match = trd_qty
        self.trade_entry_request.set_default_execution_summary(order_id1,
                                                               [execution_report_co_order_id],
                                                               self.price, qty_to_match)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # Step 10 - Verify GTW has 35=8 with 39=B, 150=B, 31=5, 44=5
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
                                  'SettlCurrency', 'StrategyName', 'ReplyReceivedTime', 'AvgPx', 'ExecType', 'Parties',
                                  'TradeReportingIndicator', 'ClOrdID']
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({'LastPx': '5', 'Price': '5'})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ignored_fields=list_of_ignored_fields)

        self.exec_report.set_default_calculated(self.fix_message2)
        self.exec_report.change_parameters({'LastPx': '5', 'Price': '5'})
        self.fix_verifier.check_fix_message_fix_standard(
            self.exec_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def _set_manual_disclose_exec(self, order_id):
        self.order_action_request.set_default([order_id])
        order_dict = {order_id: order_id}
        self.java_api_manager.send_message_and_receive_response(self.order_action_request, order_dict)
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id). \
            get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value},
            order_notification, f'Precondition: Verifying that DiscloseExec = M for {order_id}')