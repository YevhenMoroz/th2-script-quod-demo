import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7504(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bo_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.client_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.unallocate_request = BlockUnallocateRequest()
        self.unbook_request = BookingCancelRequest()
        self.desk_id = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        self.ord_sub_message.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                    desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                    role=SubmitRequestConst.USER_ROLE_1.value)
        response = self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        self.return_result(response, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_order_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        qty = self.result.get_parameter('OrdReplyBlock')['OrdQty']
        price = self.result.get_parameter('OrdReplyBlock')['Price']
        # endregion
        # region trade order
        self.trade_entry_message.set_default_trade(order_id, price, qty)
        self.java_api_manager.send_message(self.trade_entry_message)
        # endregion
        # region complete order
        self.complete_order.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_order)
        # endregion
        # region book order
        self.allocation_instruction.set_default_book(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        # endregion
        # region approve order
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.approve_message)
        # endregion
        # region allocate order
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.client_acc,
            'AllocQty': qty,
            'AvgPx': price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_instr_id = self.result.get_parameter('AllocationReportBlock')['BookingAllocInstructionID']
        # endregion
        # region unallocate order
        self.unallocate_request.set_default(alloc_id)
        self.java_api_manager.send_message(self.unallocate_request)
        # endregion
        # region check Confirmation Report
        params = {'ConfirmTransType': "2", 'AllocAccount': self.client_acc, 'NoOrders': [{
            'ClOrdID': cl_order_id,
            'OrderID': order_id
        }]}
        ignored_fields_conf_report = ['AllocQty', 'ConfirmType', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                                      'BookID', 'SettlDate', 'AllocID', 'Currency', 'NetMoney', 'MatchStatus',
                                      'ConfirmStatus', 'TradeDate', 'NoParty', 'AllocInstructionMiscBlock1', 'tag5120',
                                      'CpctyConfGrp', 'ReportedPx', 'Instrument', 'GrossTradeAmt', 'ConfirmID',
                                      'OrderAvgPx', 'tag11245', 'AllocInstructionMiscBlock2']
        conf_report = FixMessageConfirmationReportOMS(self.data_set, params)
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=ignored_fields_conf_report)
        # endregion
        # region unbook order
        self.unbook_request.set_default(alloc_instr_id)
        self.java_api_manager.send_message(self.unbook_request)
        # endregion
        # region check Allocation Report 626=2
        new_params = {'Account': self.client_acc,
                      'AllocTransType': '2',
                      'AllocType': '2', 'NoOrders': [{
                'ClOrdID': cl_order_id,
                'OrderID': order_id
            }]}
        ignored_fields_alloc_report = ["Account", "TransactTime", "Side", "AvgPx", "QuodTradeQualifier", "BookID",
                                       "SettlDate", "AllocID", "Currency", "NetMoney", "TradeDate", "BookingType",
                                       "NoAllocs", "NoParty", "AllocInstructionMiscBlock1", "Quantity", "tag5120",
                                       "ReportedPx", "Instrument", "RootSettlCurrAmt", "GrossTradeAmt", 'OrderAvgPx',
                                       'ExecAllocGrp']
        alloc_report = FixMessageAllocationInstructionReportOMS(new_params)
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ['AllocTransType', 'AllocType'],
                                                            ignored_fields=ignored_fields_alloc_report)
        # endregion
        # region check Allocation Report 626=5
        new_params = {'Account': self.client_acc,
                      'AllocTransType': '2',
                      'AllocType': '5', 'NoOrders': [{
                'ClOrdID': cl_order_id,
                'OrderID': order_id
            }]}
        alloc_report = FixMessageAllocationInstructionReportOMS(new_params)
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ['AllocTransType', 'AllocType'],
                                                            ignored_fields=ignored_fields_alloc_report)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
