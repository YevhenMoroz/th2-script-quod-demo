import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationInstructionConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7189(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '300'
        self.price = '20'
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.currency_major = self.data_set.get_currency_by_name('currency_2')  # GBP
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')  # MOClient_EUREX
        self.venue = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.client = self.data_set.get_client('client_com_1')  #
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message()
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA order step 1 and step 2 and step 3
        self.order_submit.set_default_dma_limit()
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Creating DMA order ", responses)

        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_2"),
            "OrdQty": self.qty,
            "LastTradedQty": self.qty,
            "LastPx": self.price,
            "Price": self.price,
            "Currency": self.currency,
            "LeavesQty": 0,
            "CumQty": self.qty,
            "AvgPrice": self.price
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Partially executing DMA order", responses)
        rate_and_amt = str(1 / 100)
        execution_result = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_sts_expected = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}
        self.java_api_manager.compare_values(exec_sts_expected, execution_result,
                                             'Check actually and expected result from step 2',
                                             VerificationMethod.CONTAINS)
        expected_result = {
            JavaApiFields.CommissionRate.value: rate_and_amt,
            JavaApiFields.CommissionCurrency.value: self.currency_major,
            JavaApiFields.CommissionAmount.value: rate_and_amt,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value
        }

        self.java_api_manager.compare_values(expected_result, execution_result[JavaApiFields.ClientCommissionList.value][
                JavaApiFields.ClientCommissionBlock.value][0],
                                             f'Check that client commission has {self.currency_major} currency (step 3)',
                                             VerificationMethod.CONTAINS)
        # endregion
