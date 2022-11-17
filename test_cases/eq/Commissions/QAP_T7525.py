import logging
import os
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationInstructionConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7525(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "3285"
        self.price = "3285"
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.commisison_currency = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.commission_profile = self.data_set.get_comm_profile_by_name('per_u_qty')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        time.sleep(10)
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client,
                                                                         comm_profile=self.commission_profile).send_post_request()
        time.sleep(10)
        self.__trade_dma_order_and_check_actually_result(self.__send_dma_order())

    def __send_dma_order(self):
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        return order_id
        # endregion

    def __trade_dma_order_and_check_actually_result(self, order_id):
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": self.qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": 0,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Fully filled)', responses)
        commission_rate = "0.5"
        commission_amount = str(float(float(commission_rate) * int(self.qty)) / 100)
        expected_result = {JavaApiFields.CommissionCurrency.value: self.commisison_currency,
                           JavaApiFields.CommissionAmount.value: commission_amount,
                           JavaApiFields.CommissionRate.value: commission_rate,
                           JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
                           JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_UNI.value}
        actualy_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                ExecutionReportConst.ExecType_TRD.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(expected_result, actualy_result,
                                             'Comparing actually and expected result from last step')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
