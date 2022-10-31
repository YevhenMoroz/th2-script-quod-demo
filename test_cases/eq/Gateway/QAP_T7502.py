import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from datetime import datetime, timedelta
from pandas import Timestamp as tm
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7502(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.unallocate_request = BlockUnallocateRequest()
        self.qty = '300'
        self.result = None
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7502
        # region create CO  order (precondition)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price}
                                                       )

        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_ord_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        status = self.result.get_parameter('OrdReplyBlock')['TransStatus']
        self.order_book.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            f'Comparing {OrderBookColumns.sts.value}')

        # endregion

        # region step 1 and step 2, step 3( trade CO order)
        qty_for_trade = str(int(self.qty) / 2)
        settl_date = (tm(datetime.utcnow().isoformat()) + timedelta(days=1)).date()
        settl_date_check_exec_message = settl_date.strftime('%Y%m%d')
        for i in range(2):
            self.trade_entry_message.set_default_trade(order_id, self.price, qty_for_trade)
            self.trade_entry_message.update_fields_in_component('TradeEntryRequestBlock',
                                                                {'SettlDate': settl_date.strftime(
                                                                    '%Y-%m-%dT%H:%M:%S')})
            responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
            class_name.print_message(f'TRADE {i + 1} time', responses)
            self.return_result(responses, ORSMessageType.ExecutionReport.value)
            actually_result = self.result.get_parameters()['ExecutionReportBlock']['TransExecStatus']
            expected_result: dict = {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value}
            if i == 0:
                expected_result.update(
                    {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_PFL.value})
            self.order_book.compare_values(
                expected_result,
                {OrderBookColumns.exec_sts.value: actually_result},
                f'Comparing {OrderBookColumns.exec_sts.value}')

        # endregion

        # region step 4 check 35=8 (39=2 and 39=1) message
        change_parameters = {
            'ClOrdID': cl_ord_id
        }
        list_of_ignored_fields = ['Account', 'ExecID', 'tag5120', 'OrderQtyData',
                                  'LastQty', 'OrderID', 'TimeInForce', 'PositionEffect',
                                  'HandlInst', 'CumQty', 'LastPx', 'OrdType',
                                  'LastMkt', 'OrderCapacity', 'QtyType', 'ExecBroker',
                                  'Price', 'VenueType', 'ExDestination', 'GrossTradeAmt',
                                  'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                                  'BookID', 'Currency', 'TradeDate', 'LeavesQty', 'NoParty', 'Instrument']
        execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        execution_report.change_parameters({'ExecType': 'F', "OrdStatus": "1",
                                            'LeavesQty': qty_for_trade, 'SettlDate': settl_date_check_exec_message})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        execution_report.change_parameters({"OrdStatus": "2", 'LeavesQty': 0})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
                break

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
