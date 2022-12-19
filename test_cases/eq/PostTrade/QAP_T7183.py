import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7183(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.comp_commission_and_fee_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client('client_pt_1')
        self.order_submit = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.qty = '200'
        self.price = '20'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition

        # part 1: Set up ClientCommission with minimal value
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name('commission_with_minimal_value'), client=self.client)
        self.rest_commission_sender.send_post_request()
        # end of part

        # part 2 create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty,
             "AccountGroupID": self.client,
             "Price": self.price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # end of part

        # part 3 execute DMA order
        list_of_exec_id = []
        self.execution_report.set_default_trade(order_id)
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
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value:
                                                  ExecutionReportConst.TransExecStatus_FIL.value},
                                             execution_report_message,
                                             f'Checking expected and actually results of {order_id} '
                                             f'(ExecSts)')
        self.java_api_manager.compare_values({JavaApiFields.PostTradeStatus.value:
                                                  post_trade_sts},
                                             order_reply,
                                             f'Checking expected and actually results of {order_id} '
                                             '(PostTradeStatus)')
        # end of part

        # endregion

        # region step 1 and step 2
        self.comp_commission_and_fee_request.set_list_of_order_alloc_block(cl_ord_id, order_id, post_trade_sts)
        self.comp_commission_and_fee_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trade_sts)
        self.comp_commission_and_fee_request.set_default_compute_booking_request(self.qty, self.price, self.client)
        self.java_api_manager.send_message_and_receive_response(self.comp_commission_and_fee_request)
        # endregion
        compute_commission_misc_fee_reply = self.java_api_manager.get_last_message(ORSMessageType.
                                                                                   ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.CommissionAmount.value: str(float(100))},
                                             compute_commission_misc_fee_reply[
                                                 JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Checking expected and actually result (step 2)')
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
