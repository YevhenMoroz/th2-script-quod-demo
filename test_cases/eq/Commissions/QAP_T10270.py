import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiSubmitAdminCommand import RestApiSubmitAdminCommandBlock
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10270(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "10"
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_venue_by_name("venue_1")  # PARIS
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.cur = self.data_set.get_currency_by_name('currency_1')
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.system_command = RestApiSubmitAdminCommandBlock()
        self.rest_api_manager = RestApiManager(session_alias=self.wa_connectivity, case_id=self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fee
        params = {"venueID": self.venue}
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt, client=self.client)
        self.rest_commission_sender.change_message_params(params)
        self.rest_commission_sender.send_post_request()
        # endregion

        # region Create order
        self.nos.update_fields_in_component("NewOrderReplyBlock",
                                            {"VenueAccount": {"VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep["OrdID"]
        cl_ord_id = self.nos.get_parameter("NewOrderReplyBlock")["ClOrdID"]
        expected_result = {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y"}
        actually_result = {JavaApiFields.TransStatus.value: ord_rep[JavaApiFields.TransStatus.value],
                           JavaApiFields.UnsolicitedOrder.value: ord_rep[JavaApiFields.UnsolicitedOrder.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check order status')
        # endregion

        comm_list = {
            JavaApiFields.CommissionBasis.value: 'PCT',
            JavaApiFields.CommissionAmount.value: '50.0',
            JavaApiFields.CommissionRate.value: '5.0',
            JavaApiFields.CommissionAmountType.value: 'BRK',
            JavaApiFields.CommissionCurrency.value: self.cur
        }

        # region execute order
        self.exec_rep.set_default_trade(cl_ord_id)
        self.exec_rep.update_fields_in_component('ExecutionReportBlock', {"LeavesQty": "50.0",
                                                                          "CumQty": "50.0", "LastTradedQty": "50.0"})
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, {"OrdID": order_id})
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
                           JavaApiFields.ClientCommissionList.value: {
                               JavaApiFields.ClientCommissionBlock.value: [comm_list]}}
        self.java_api_manager.compare_values(expected_result, exec_report, 'Check execution status and commission')
        # endregion

        # region complete order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report,
            'Check order after complete')
        # endregion

        # region sent UnsetDoneForDay
        self.system_command.set_default_param("ESBUYTH2TEST", "UDD", "VenueID", self.venue)
        self.rest_api_manager.send_post_request(self.system_command)
        # endregion

        # region complete order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report,
            'Check order after complete')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
