import logging
import os
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7443(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '49540'
        price = '0.789'
        value_for_commission = '0.1'
        value_for_fee = '1'
        account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        venue_client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        trade_rule = None
        new_order_single_rule = None
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create DMA order (step 1, step 2)
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       venue_client,
                                                                                       exec_destination,
                                                                                       float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.test_id, status='FAIL')

        finally:
            time.sleep(5)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        exec_sts = self.order_book.extract_field(OrderBookColumns.exec_sts.value)
        self.__comparing_values({OrderBookColumns.post_trade_status.value: 'ReadyBooked',
                                 OrderBookColumns.exec_sts.value: 'Filled'},
                                {OrderBookColumns.post_trade_status.value: post_trade_status,
                                 OrderBookColumns.exec_sts.value: exec_sts},
                                'Comparing post trade status after book', 'self.order_book.compare_values')
        # endregion

        # region book order (3 step)
        allocation_instruction_message = FixMessageAllocationInstructionReportOMS()
        allocation_instruction_message.set_default_ready_to_book(self.fix_message)
        allocation_instruction_message.add_tag({'RootCommTypeClCommBasis': '*'}). \
            add_tag({'RootOrClientCommissionCurrency': '*'}).add_tag({'RootSettlCurrFxRate': '*'}). \
            add_tag({'RootSettlCurrAmt': '39127.14706'}).add_tag({'RootOrClientCommission': '*'}). \
            add_tag({'NoRootMiscFeesList': [{'RootMiscFeeBasis': '*', 'RootMiscFeeCurr': '*', 'RootMiscFeeType': '*',
                                             'RootMiscFeeRate': value_for_fee, 'RootMiscFeeAmt': value_for_fee}]})
        fee_basis = self.data_set.get_commission_basis('comm_basis_1')
        commission_basis = self.data_set.get_commission_basis('comm_basis_2')
        self.middle_office.set_modify_ticket_details(comm_basis=commission_basis, comm_rate=value_for_commission,
                                                     fee_basis=fee_basis,
                                                     fee_rate=value_for_fee,
                                                     fee_type=self.data_set.get_misc_fee_type_by_name('tax'),
                                                     extract_book=True,
                                                     toggle_manual=True)
        values = self.middle_office.book_order()
        fix_verifier.check_fix_message_fix_standard(allocation_instruction_message)
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        filter_list = [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]]
        # endregion

        # region approve and allocate block (step 4)
        self.middle_office.approve_block()
        confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_message.set_default_confirmation_new(self.fix_message)
        confirmation_message.add_tag({'Account': '*'}).add_tag({'SettlCurrFxRate': '*'}). \
            add_tag({'AllocInstructionMiscBlock2': '*'}).add_tag({'tag5120':'*'}).\
            add_tag({'NoMiscFees': [{'MiscFeeAmt': value_for_fee, 'MiscFeeCurr': '*', 'MiscFeeType': '*'}]}).\
            add_tag({'CommissionData': {'CommissionType': '3', 'Commission': '39.08', 'CommCurrency': '*'}})
        arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=arr_allocation_param)
        self.middle_office.allocate_block(filter_list)
        fix_verifier.check_fix_message_fix_standard(confirmation_message)
        # endregion

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)
