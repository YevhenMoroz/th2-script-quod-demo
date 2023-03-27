import logging
import time

from custom import basic_custom_actions as bca
from pathlib import Path
from datetime import datetime
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationInstructionConst
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


class QAP_T7357(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "4535"
        self.price = "4535"
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.major_currency = self.data_set.get_currency_by_name('currency_2')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.misc_fee_rate = '0.01'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        time.sleep(5)
        fee_profile = self.data_set.get_comm_profile_by_name('abs_amt')
        self.rest_commission_sender.set_modify_fees_message(fee_type=self.data_set.get_misc_fee_type_by_name("agent"),
                                                            comm_profile=fee_profile)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': self.data_set.get_fee_exec_scope_by_name("first_exec"),
             "venueID": self.data_set.get_venue_by_name("venue_2")})
        self.rest_commission_sender.send_post_request()
        time.sleep(5)
        self.__partially_filled_dma_orders_and_check_result(self.__send_dma_orders())
        self.__fully_filled_order_and_check_result()

    def __send_dma_orders(self):
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

    def __partially_filled_dma_orders_and_check_result(self, order_id):
        self.execution_report.set_default_trade(order_id)
        self.half_qty = int(int(self.qty) / 2)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": self.half_qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": self.half_qty,
                                                             "CumQty": self.half_qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Partially filled)', responses)
        actually_result: dict = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value][JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0]
        actually_result.update({JavaApiFields.TransExecStatus.value:
                                    self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
                               get_parameters()[JavaApiFields.ExecutionReportBlock.value][
                                        JavaApiFields.TransExecStatus.value]})
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
                           JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value,
                           JavaApiFields.MiscFeeCurr.value: self.major_currency,
                           JavaApiFields.MiscFeeAmt.value: self.misc_fee_rate,
                           JavaApiFields.MiscFeeRate.value: self.misc_fee_rate}
        self.java_api_manager.compare_values(actually_result, expected_result, 'Comparing result from step 2')

    def __fully_filled_order_and_check_result(self):
        qty_trade = str(int(self.qty) - int(self.half_qty))
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {"LeavesQty": 0, "CumQty": qty_trade,
                                                          'LastTradedQty': qty_trade,
                                                          "VenueExecID": bca.client_orderid(9),
                                                          "LastVenueOrdID": (
                                                                  tm(datetime.utcnow().isoformat()) + bd(
                                                              n=2)).date().strftime(
                                                              '%Y-%m-%dT%H:%M:%S'),
                                                          })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Fully Filled)', responses)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_TRD.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        trans_exec = {JavaApiFields.TransExecStatus.value: actually_result[JavaApiFields.TransExecStatus.value]}
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}
        self.java_api_manager.compare_values(expected_result, trans_exec, 'Comparing result from step 3')
        fee_is_absent = not (JavaApiFields.MiscFeesList.value in actually_result)
        self.java_api_manager.compare_values({'FeeIsAbsent': True}, {'FeeIsAbsent': fee_is_absent},
                                             'Verifying that MiscFee doesn`t present for second execution')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
