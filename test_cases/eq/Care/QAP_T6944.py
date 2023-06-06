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
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6944(TestCase):
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
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_3')
        self.firm_account = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.unmatch_request = UnMatchRequest()
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step precondition : Create CO order and split its and partially filled child DMA order
        # part 1: Create CO order
        self.new_order_single.set_default_care_limit()
        self.new_order_single.change_parameters({'Account': self.client})
        qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        price = self.new_order_single.get_parameter('Price')
        self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        cl_ord_id = self.new_order_single.get_parameter('ClOrdID')
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
                JavaApiFields.ListingList.value: {
                    JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing}]},
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
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.CumQty.value: '0.0'},
                                             execution_report,
                                             'Verify that order has open status (step 1)')
        # endregion

        # region step 2-3:
        execution_report_pos = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_POS.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        position_transfer_id = execution_report_pos[JavaApiFields.PositionTransferID.value]
        # endregion

        # region step 2: Check that on SellSide gateway only 35=8(150=H,39=0) message sent after unmatch and Transfer
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix_position = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix.change_parameters({"ExecType": "H", "ClOrdID": cl_ord_id})
        self.fix_verifier_ss.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                    pre_filter={
                                                        "ExecType": "F",
                                                        "ClOrdID": position_transfer_id
                                                    })

        ignored_fields = ['Account', 'ExecID', 'GatingRuleCondName', 'OrderQtyData',
                          'ExecRefID', 'LastQty', 'GatingRuleName', 'OrderID',
                          'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                          'OrdStatus', 'SettlCurrency', 'SettlDate', 'LastExecutionPolicy',
                          'Currency', 'TimeInForce', 'TradeDate', 'HandlInst',
                          'LeavesQty', 'NoParty', 'CumQty', 'LastPx', 'OrdType', 'tag5120',
                          'LastMkt', 'OrderCapacity', 'QtyType', 'ExecBroker', 'Price',
                          'Instrument', 'SecondaryExecID', 'ExDestination', 'GrossTradeAmt', 'TrdType',
                          'Parties', 'TradeReportingIndicator', 'VenueType']
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ['ExecType', 'ClOrdID'],
                                                            ignored_fields=ignored_fields)
        # endregion

        # region step 3: Check that ORS sends to BO gateway TradeCancel  and PositionTrade message
        execution_report_fix_position.change_parameters({"ExecType": "F",
                                                         "ClOrdID": position_transfer_id})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ['ExecType', 'ClOrdID'],
                                                            ignored_fields=ignored_fields)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix_position, ['ExecType', 'ClOrdID'],
                                                            ignored_fields=ignored_fields)
        # endregion

        # region step 4: Do house fill
        self.trade_entry.set_default_house_fill(order_id, self.wash_book, price, first_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_report_trade = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                        ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report_trade, 'Verify that CO order is Partially Fill (step 3)')
        exec_id_house_fill = execution_report_trade[JavaApiFields.ExecID.value]
        # endregion

        # region step 5: Check, that only trade message(35=8 150=F and 39=1) sent on SellGate way:
        pos_exec_id = \
            self.db_manager.execute_query(
                f"SELECT execid FROM execution WHERE exectype='POS' AND transid='{order_id}'")[0][0]
        ignored_fields.remove('ExecID')
        ignored_fields.remove('OrdStatus')
        filter_list = ['ExecType', 'ClOrdID', 'OrdStatus', 'ExecID']
        execution_report_fix.change_parameters(
            {"ExecType": "F", "ClOrdID": cl_ord_id, 'OrdStatus': '1', 'ExecID': exec_id_house_fill})
        self.fix_verifier_ss.check_fix_message_fix_standard(execution_report_fix,
                                                            filter_list, ignored_fields=ignored_fields)
        pre_filter = {"ExecType": "F", "ExecID": pos_exec_id, "ClOrdID": cl_ord_id, 'OrdStatus': '2'}
        self.fix_verifier_ss.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                    pre_filter=pre_filter)

        # endregion

        # region step 6: Check that 35=8(ExecType = PositionTrade) and 35=8(ExecType = Trade) messages sent to BO
        execution_report_fix_position.change_parameters(pre_filter)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix,
                                                            filter_list, ignored_fields=ignored_fields)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix_position,
                                                            filter_list, ignored_fields=ignored_fields)
        # endregion

        # region step 7: amend house fill
        new_price = str(float(price) + 1)
        self.trade_entry.set_default_amend_house_fill(order_id, first_qty, new_price, self.wash_book,
                                                      exec_id_house_fill)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_report_trade = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                        OrderReplyConst.ExecType_COR.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id_amend_house_fill = execution_report_trade[JavaApiFields.ExecID.value]
        # endregion

        # region step 8:
        execution_report_fix.change_parameters(
            {"ExecType": "G", 'ExecID': exec_id_amend_house_fill, 'LastPx': new_price})
        self.fix_verifier_ss.check_fix_message_fix_standard(execution_report_fix,
                                                            filter_list, ignored_fields=ignored_fields)
        pos_exec_id_amend = self.db_manager.execute_query(
            f"SELECT execid FROM execution WHERE exectype='PCO' AND transid='{order_id}'")[0][0]
        pre_filter.update({"ExecType": "G", 'ExecID': pos_exec_id_amend, 'LastPx': new_price})
        self.fix_verifier_ss.check_no_message_found(message_timeout=10000, message_name='ExecutionReport',
                                                    pre_filter=pre_filter)

        execution_report_fix_position.change_parameters(pre_filter)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix,
                                                            filter_list, ignored_fields=ignored_fields)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix_position,
                                                            filter_list, ignored_fields=ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.close_connection()



