import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7035(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty = '1000'
        self.price = '10'
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_com_1')
        self.currency_major = self.data_set.get_currency_by_name('currency_2')
        self.fix_message_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.cancer_request = CancelOrderRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('regulatory')
        commission_profile = self.data_set.get_comm_profile_by_name('bas_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_fees()
        time.sleep(10)
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        time.sleep(10)
        # endregion

        # region create DMA  partially and partially filled  (step 1 and step 2)
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
        half_qty = str(int(int(self.qty) / 2))
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_2"),
            "OrdQty": self.qty,
            "LastTradedQty": half_qty,
            "LastPx": self.price,
            "Price": self.price,
            "Currency": self.currency,
            "LeavesQty": half_qty,
            "CumQty": half_qty,
            "AvgPrice": self.price
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Partially executing DMA order", responses)
        # endregion

        # region check expected result from step 2
        expected_result = ExecutionReportConst.TransExecStatus_PFL.value
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.TransExecStatus.value]
        self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value: expected_result},
                                             {JavaApiFields.TransExecStatus.value: actually_result},
                                             'Comparing value from step 2')
        # endregion

        # region step 3 cancelling order via FE request
        self.cancer_request.set_default(order_id)
        try:
            cancel_request = self.rule_manager.add_OrderCancelRequest(self.bs_connectivity, self.venue_client_name,
                                                                      self.venue, True, 0)
            responses = self.java_api_manager.send_message_and_receive_response(self.cancer_request)
        except Exception as e:
            logger.error(f"Your exception is {e}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_request)

        print_message("Canceling DMA order ", responses)
        # endregion

        # region check expected result from step 3
        expected_result = OrderReplyConst.TransStatus_CXL.value
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        cl_ord_id = order_reply_message[JavaApiFields.ClOrdID.value]
        actually_result = order_reply_message[JavaApiFields.TransStatus.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: expected_result},
                                             {JavaApiFields.TransStatus.value: actually_result},
                                             'Comparing value from step 2')
        # endregion

        # region check 35=8 150 = B message
        list_of_ignore_fields = ['SecondaryOrderID', 'LastExecutionPolicy', 'TradeDate', 'SecondaryExecID', 'OrderID',
                                 'ExDestination', 'GrossTradeAmt', 'SettlCurrency', 'Instrument', 'TimeInForce',
                                 'OrdType', "TradeReportingIndicator", 'SettlDate', 'Side', 'HandlInst', 'OrderQtyData',
                                 'SecondaryExecID', 'ExecID', 'LastQty', 'TransactTime', 'AvgPx', 'QuodTradeQualifier',
                                 'BookID', 'Currency', 'PositionEffect', 'TrdType', 'LeavesQty', 'NoParty', 'CumQty',
                                 'LastPx', 'LastCapacity', 'tag5120', 'LastMkt', 'OrderCapacity''QtyType', 'ExecBroker',
                                 'QtyType', 'Price', 'OrderCapacity', 'VenueType', 'CommissionData', 'Text',
                                 'AllocQty', 'ConfirmType', 'ConfirmID','Account',
                                 'AllocID', 'NetMoney', 'MatchStatus',
                                 'ConfirmStatus', 'AllocInstructionMiscBlock1',
                                 'CpctyConfGrp', 'ReportedPx']
        self.fix_message_execution_report.change_parameters({
            "ExecType": "B",
            "OrdStatus": "B",
            "ClOrdID": cl_ord_id})
        amount = str(round((1 / 1000000) * 5000, 3))
        self.fix_message_execution_report.change_parameters({'QuodTradeQualifier': '*', 'BookID': '*',
                                                             'Currency': self.currency, 'NoParty': '*',
                                                             'CommissionData': '*',
                                                             'tag5120': '*', 'SecondaryOrderID': "*", 'ExecBroker': '*',
                                                             'NoMiscFees': [{
                                                                 'MiscFeeAmt': amount,
                                                                 'MiscFeeCurr': self.currency_major,
                                                                 'MiscFeeType': '1'
                                                             }]})
        self.fix_verifier.check_fix_message_fix_standard(self.fix_message_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
