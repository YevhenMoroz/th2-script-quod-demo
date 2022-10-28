import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7149(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = self.fix_message.get_parameter("Price")
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm = self.data_set.get_commission_by_name("commission1")
        self.comm_profile = self.data_set.get_comm_profile_by_name("abs_amt_2")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.comm_rate = "1.55"
        self.comm_basis = self.data_set.get_commission_basis('comm_basis_1')
        self.comp_comm = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(commission=self.comm,
                                                                         account=self.client_acc,
                                                                         comm_profile=self.comm_profile).send_post_request()
        # endregion

        # region send order
        self.__send_fix_orders()
        # endregion

        # region Check ExecutionReports
        self.exec_report.set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region get values from booking ticket
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.comp_comm.set_list_of_order_alloc_block(self.cl_order_id, self.order_id, post_trade_sts)
        self.comp_comm.set_list_of_exec_alloc_block(self.qty, self.exec_id, self.price, post_trade_sts)
        self.comp_comm.set_default_compute_booking_request(self.qty)
        self.comp_comm.update_fields_in_component(JavaApiFields.ComputeBookingFeesCommissionsRequestBlock.value,
                                                  {'AccountGroupID': self.client, 'AvgPx': '0.100000000'})
        responses = self.java_api_manager.send_message_and_receive_response(self.comp_comm)
        self.__return_result(responses, ORSMessageType.ComputeBookingFeesCommissionsReply.value)
        comm_list_exp = None
        comm_list = self.result.get_parameter(JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[
            'ClientCommissionList']
        # print(comm_list)
        # endregion

        # region book order
        self.allocation_instruction.set_default_book(self.order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.cur,
                                                                   "AccountGroupID": self.client,
                                                                   'ClientCommissionList': comm_list
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion

        # region check block values
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        alloc_inst_id = alloc_report['ClientAllocID']
        self.java_api_manager.compare_values({'ClientCommissionList': comm_list_exp}, alloc_report,
                                             "Check values in the Alloc Report")
        # endregion

        # region approve block
        self.approve.set_default_approve(alloc_inst_id)
        self.java_api_manager.send_message(self.approve)
        # endregion

        # region allocate block
        self.confirmation.set_default_allocation(alloc_inst_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock',
                                                     {'AllocAccountID': self.client_acc, "InstrID": instrument_id,
                                                      "AvgPx": self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation)
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        self.java_api_manager.compare_values({'ClientCommissionList': comm_list_exp}, alloc_report,
                                             "Check fees in the Alloc Report after allocation")
        comm_list_in_alloc = None
        self.__return_result(responses, ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.AffirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             'ClientCommissionList': comm_list_exp},
            self.result.get_parameter(JavaApiFields.ConfirmationReportBlock.value),
            'Check block sts in the Confirmation')
        conf_id = self.result.get_parameter(JavaApiFields.ConfirmationReportBlock.value)['ConfirmationID']
        # endregion

        # region check allocation commission 1
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        comm_data_1 = {"CommissionType": '3', "Commission": "0",
                       "CommCurrency": self.com_cur}
        conf_report.change_parameters(
            {"AllocQty": self.qty, "Account": self.client, "AllocAccount": self.client_acc, "AvgPx": "*",
             "Currency": "*", "tag5120": "*",
             "CommissionData": comm_data_1, 'NoOrders': [{'ClOrdID': self.cl_order_id, "OrderID": self.order_id}]})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ["OrderID"])
        # endregion

        # region amend allocation
        self.confirmation.set_default_amend_allocation(conf_id, alloc_inst_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock',
                                                     {'AllocAccountID': self.client_acc, "InstrID": instrument_id,
                                                       })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation)
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        self.java_api_manager.compare_values({'ClientCommissionList': comm_list_exp}, alloc_report,
                                             "Check fees in the Alloc Report after allocation")
        # endregion

        # region check amended allocation commission
        comm_data_2 = {"CommissionType": '3', "Commission": self.comm_rate,
                       "CommCurrency": self.com_cur}
        conf_report2 = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_replace(self.fix_message)
        conf_report2.change_parameters(
            {"AllocQty": self.qty, "Account": self.client, "AllocAccount": self.client_acc, "AvgPx": "*",
             "Currency": "*", "tag5120": "*", "CommissionData": comm_data_2,
             'NoOrders': [{'ClOrdID': self.cl_order_id, "OrderID": self.order_id}]})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report2, ["OrderID", "ConfirmTransType"])
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 "ExDestination": self.mic,
                 "Currency": self.data_set.get_currency_by_name("currency_3")})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            self.order_id = self.response[0].get_parameter("OrderID")
            self.cl_order_id = self.response[0].get_parameter("ClOrdID")
            self.exec_id = self.response[1].get_parameter("ExecID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
