import logging
import os
from pathlib import Path

from custom.basic_custom_actions import create_event
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7497(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "3350"
        self.price = "3350"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.abs_amt_profile = self.data_set.get_comm_profile_by_name("abs_amt_2")
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.dfd_management_request = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(account=self.account,
                                                                         comm_profile=self.abs_amt_profile
                                                                         ).send_post_request()
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        message = 'Check values after manual execution'
        QAP_T7497.print_message('Message after manual execution of order', responses)
        self.__verify_commissions(message)
        self.dfd_management_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.dfd_management_request)
        QAP_T7497.print_message('Message after complete of order', responses)
        message = 'Check values of execution after complete'
        self.__verify_commissions(message)
        message = 'Check values of order after complete'
        self.__verify_order_value(message)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(
            "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2"),
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)

    def __verify_commissions(self, message):
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ClientCommission.value: "1.0E-5"}, actually_result,
                                             event_name=message)

    def __verify_order_value(self, message):
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, actually_result,
            message)

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
