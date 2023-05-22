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
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, AllocationInstructionConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7173(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_com_1')
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
        self.rest_api_manager = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        self.qty = '300'
        self.result = None
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up commission and fees
        fee = '0.01'
        commission = '1.5'
        fee_rate = '0.01'
        commission_rate = '0.5'
        self.rest_api_manager.clear_fees()
        self.rest_api_manager.clear_commissions()
        self.rest_api_manager.send_default_fee()
        self.rest_api_manager.set_modify_client_commission_message(account=self.client,
                                                                   comm_profile=self.data_set.get_comm_profile_by_name(
                                                                       'per_u_qty')).send_post_request()
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        listing_id = self.data_set.get_listing_id_by_name("listing_2")
        # endregion

        # region create CO  order (precondition)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price,
                                                        'ListingList': {'ListingBlock': [{'ListingID': listing_id}]},
                                                        'InstrID': instrument_id
                                                        }
                                                       )
        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_ord_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        # endregion

        # region execute CO order
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager.send_message(self.trade_entry_message)
        # endregion

        # region complete CO order
        self.java_api_manager.send_message(
            self.complete_order.set_default_complete(order_id))
        # endregion

        # region book and approve CO order
        gross_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.set_default_book(order_id)
        currency_GBP = self.data_set.get_currency_by_name('currency_2')
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.data_set.get_currency_by_name(
                                                                       "currency_3"),
                                                                   "AccountGroupID": self.client,
                                                                   'RootMiscFeesList': {'RootMiscFeesBlock': [
                                                                       {
                                                                           'RootMiscFeeType': AllocationInstructionConst.RootMiscFeeType_EXC.value,
                                                                           'RootMiscFeeAmt': fee,
                                                                           'RootMiscFeeCurr': currency_GBP,
                                                                           'RootMiscFeeBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value,
                                                                           'RootMiscFeeRate': fee_rate
                                                                       }
                                                                   ]},
                                                                   'ClientCommissionList': {
                                                                       'ClientCommissionBlock': [{
                                                                           'CommissionAmountType': AllocationInstructionConst.CommissionAmountType_BRK.value,
                                                                           'CommissionAmount': commission,
                                                                           'CommissionBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_UNI.value,
                                                                           'CommissionCurrency': currency_GBP,
                                                                           'CommissionRate': commission_rate
                                                                       }]
                                                                   }
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.approve_message)
        # endregion

        # region allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                             {'InstrID': instrument_id})
        sec_acc_1 = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": sec_acc_1,
            'AllocQty': self.qty,
            'AvgPx': self.price,
        })
        self.java_api_manager.send_message(self.confirmation_request)
        # endregion

        # region step 1
        change_parameters = {'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': '*'
        }], 'AllocAccount': sec_acc_1,
            'ConfirmTransType': '0',
            'CommissionData': {
                'Commission': commission
            },
            'NoMiscFees': [{
                'MiscFeeAmt': fee
            }]
        }
        list_of_ignored_fields = [
            'AllocQty', 'ConfirmType', 'TransactTime',
            'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
            'SettlDate', 'AllocID', 'Currency', 'NetMoney',
            'MatchStatus', 'ConfirmStatus', 'TradeDate',
            'NoParty', 'AllocInstructionMiscBlock1', 'tag5120',
            'CpctyConfGrp', 'ReportedPx', 'Instrument',
            'GrossTradeAmt', 'ConfirmID',
            'MiscFeeCurr', 'MiscFeeType', 'CommCurrency', 'CommissionType', 'OrderAvgPx', 'tag11245'
        ]
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                         ['ConfirmTransType', 'AllocAccount', 'NoOrders'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions_and_steps(self):
        self.rest_api_manager.clear_commissions()
        self.rest_api_manager.clear_fees()
