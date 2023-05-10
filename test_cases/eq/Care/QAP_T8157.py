import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.PositionTransferCancelRequest import PositionTransferCancelRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8157(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.fix_verifier_ss = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_5')
        self.firm_account = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.unmatch_request = UnMatchRequest()
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.cancel_transfer = PositionTransferCancelRequest()
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step precondition : Create CO order and split its and partially filled child DMA order
        # part 1: Create CO order
        self._set_up_wash_book_rule()
        self.new_order_single.set_default_care_limit()
        self.new_order_single.change_parameters({'Account': self.client})
        qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        price = self.new_order_single.get_parameter('Price')
        self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = self.fix_manager.get_last_message("ExecutionReport").get_parameter("OrderID")
        # end_of_part

        # part 2: Create child DMA order from CO order
        instrument = self.data_set.get_instrument_id_by_name('instrument_2')
        listing = self.data_set.get_listing_id_by_name('listing_3')
        dma_order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.account,
                                                                                                  self.mic,
                                                                                                  float(price))
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.OrdQty.value: qty,
                JavaApiFields.InstrID.value: instrument,
                'ListingList': {'ListingBlock': [{'ListingID': listing}]},
                JavaApiFields.Price.value: price})
            self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=18000)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            dma_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                'Verifying that DMA order is created (precondition)')
        except Exception as e:
            logger.error(f'Something gone wrong : {e}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # end_of_part

        # part 3: Partially Filled DMA order
        self.execution_report.set_default_trade(dma_order_id)
        first_qty = str(float(int(qty) / 2))
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "OrdQty": qty,
            "LastTradedQty": first_qty,
            "LastPx": price,
            "Price": price,
            "LeavesQty": first_qty,
            "CumQty": first_qty,
            "AvgPrice": price})
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id})
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_parent_order = execution_report[JavaApiFields.ExecID.value]
        # end_of_part

        # endregion

        # region step 1: Do unmatch and transfer
        self.unmatch_request.set_default(self.data_set, exec_id_parent_order, first_qty, washbook=self.wash_book)
        self.unmatch_request.set_default_unmatch_and_transfer(self.firm_account)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        execution_report = \
            self.java_api_manager.get_last_message_by_multiple_filter(ORSMessageType.ExecutionReport.value,
                                                                      [ExecutionReportConst.ExecType_CAN.value,
                                                                       exec_id_parent_order]).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             execution_report,
                                             'Verify that order has open status (step 1)')
        # endregion

        # region step 2-3:
        execution_report_pos = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_POS.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        position_transfer_id = execution_report_pos[JavaApiFields.PositionTransferID.value]
        self.cancel_transfer.set_default(position_transfer_id)
        self.java_api_manager.send_message(self.cancel_transfer)
        # endregion

        # # region check that sellside does not have TradeCancel Execution_Report
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix.change_parameters({"ExecType": "H", "ClOrdID": position_transfer_id})
        self.fix_verifier_ss.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                    pre_filter={
                                                        "ExecType": "H",
                                                        "ClOrdID": position_transfer_id
                                                    })

        # region step 3: check that backOffice has PositionTradeCancel message:
        ignored_fields = ['NoParty', 'CumQty', 'LastPx', 'ExecID', 'OrderQtyData', 'tag5120', 'ExecRefID', 'LastQty',
                          'OrderID', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'ExecBroker', 'OrdStatus',
                          'Currency', 'Instrument', 'TrdType', 'LeavesQty', 'GrossTradeAmt']
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ['ExecType', 'ClOrdID'],
                                                            ignored_fields=ignored_fields)
        # endregion

    def _set_up_wash_book_rule(self):
        self.rest_wash_book_message.modify_wash_book_rule(client=self.client, washbook_account=self.wash_book)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_wash_book_message.clear_washbook_rule()
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
