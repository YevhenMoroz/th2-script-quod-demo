import logging

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    CommissionBasisConst, CommissionAmountTypeConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7511(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "3312"
        self.price = "3312"
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        abs_amt_usd = self.data_set.get_comm_profile_by_name("abs_amt_usd")
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client, comm_profile=abs_amt_usd)
        self.rest_commission_sender.send_post_request()
        tuple_with_clordid_and_order_id = self.__create_dma_order_via_java_api()
        self.__trade_execute_dma_order(tuple_with_clordid_and_order_id[0])

    def __create_dma_order_via_java_api(self):
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]

        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        return order_id, cl_ord_id

    def __trade_execute_dma_order(self, order_id):
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
                                                             "LeavesQty": self.qty,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message(f'Trade DMA  order {order_id}', responses)
        order_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                           JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}

        actually_result = {JavaApiFields.PostTradeStatus.value: order_reply[JavaApiFields.PostTradeStatus.value],
                           JavaApiFields.DoneForDay.value: order_reply[JavaApiFields.DoneForDay.value]}

        self.java_api_manager.compare_values(expected_result, actually_result, "Check statuses from step 1")
        commission_rate = 2
        cross_rate = float(0.509700)
        commission_amount = commission_rate * cross_rate
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_TRD.value).get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        expected_result = {JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_ABS.value,
                           JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
                           JavaApiFields.CommissionAmount.value: str(commission_amount),
                           JavaApiFields.CommissionRate.value: str(commission_amount),
                           JavaApiFields.CommissionCurrency.value: self.currency_post_trade
                           }
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             f"Check that client commission converted in {self.currency_post_trade} step 2")

