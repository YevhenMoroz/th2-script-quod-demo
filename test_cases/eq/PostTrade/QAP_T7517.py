import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ConfirmationReportConst, \
    AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7517(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.booking_cancel = BookingCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '100'
        price = '10'
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, 'Account': self.data_set.get_client_by_name('client_pt_1'),
             'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'), 'Price': price,
             'ExDestination': exec_destination})
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        # endregion

        # region create order
        order_id = None
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.test_id, status='FAIL')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region check execution
        ignored_field = ['ReplyReceivedTime', 'SettlCurrency', 'LastMkt', 'Text', 'SecurityDesc', 'Account',
                         'GatingRuleName']
        self.exec_report.set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_field)
        # endregion

        # region book order and verify values after it at order book (step 1)
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component('AllocationInstructionBlock', {
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
        responses = self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            self.result.get_parameter('OrdUpdateBlock'),
            'Check order sts')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value},
            self.result.get_parameter('AllocationReportBlock'),
            'Check block sts')
        alloc_instr_id = self.result.get_parameter('AllocationReportBlock')['BookingAllocInstructionID']
        # endregion
        # region unbook block (step 2)
        self.booking_cancel.set_default(alloc_instr_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.booking_cancel)
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
            self.result.get_parameter('OrdUpdateBlock'),
            'Check order sts')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_CXL.value},
            self.result.get_parameter('AllocationReportBlock'),
            'Check unbook sts')
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
