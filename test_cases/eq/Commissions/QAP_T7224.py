import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7224(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client = data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_1')
        self.new_order_single.change_parameters({"Account": self.client})
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.new_order_single.get_parameter('Price')
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.venue = self.data_set.get_venue_by_name('venue_1')
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt)
        self.commission_sender.change_message_params({"venueID": self.venue})
        self.commission_sender.send_post_request()
        # STEP 1
        # region create order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = response[0].get_parameter("OrderID")
        # endregion

        cl_comm_block = {JavaApiFields.CommissionAmount.value: self.qty + '.0',
                         JavaApiFields.CommissionCurrency.value: self.cur,
                         JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
                         JavaApiFields.CommissionRate.value: '5.0',
                         JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_PCT.value,
                         JavaApiFields.CommissionAmountSubType.value: AllocationInstructionConst.CommissionAmountSubType_OTH.value}

        # STEP 2
        # region do manual execution
        self.trade_entry_message.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_report = self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id = exec_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.ClientCommissionList.value: {JavaApiFields.ClientCommissionBlock.value: [cl_comm_block]}},
            exec_report,
            'Check commission after execution')
        # endregion

        # STEP 3
        # region amend manual execution
        qty_to_execution = str(int(int(self.qty) / 2))
        cl_comm_block.update({JavaApiFields.CommissionAmount.value: qty_to_execution + '.0'})
        self.trade_entry_message.set_default_replace_execution(order_id, exec_id, self.price, qty_to_execution)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_report = self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecQty.value: qty_to_execution + '.0',
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.ClientCommissionList.value: {JavaApiFields.ClientCommissionBlock.value: [cl_comm_block]}}, exec_report,
            'Check commission after execution modification')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
