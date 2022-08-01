import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_T7359(TestCase):
    def __init__(self, report_id, session_id, data_set):
        super().__init__(report_id, session_id, data_set)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        fix_manager = FixManager(ss_connectivity)
        qty = '5000'
        fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        fix_message.set_default_dma_limit()
        fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_8'))
        change_params = {'PreAllocGrp': {
            'NoAllocs': [{
                'AllocAccount': self.data_set.get_account_by_name('client_pt_7_acc_1'),
                'AllocQty': qty}]}}
        fix_message.change_parameters(change_params)
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        price = fix_message.get_parameter('Price')
        extract_sts = MiddleOfficeColumns.sts.value
        extract_sts_match_status = MiddleOfficeColumns.match_status.value
        extract_summary_status = MiddleOfficeColumns.summary_status.value
        block_id = MiddleOfficeColumns.block_id.value

        # endregion
        # region create 2 DMA order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                             client_for_rule,
                                                                                             exec_destination,
                                                                                             float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(bs_connectivity,
                                                                                       client_for_rule,
                                                                                       exec_destination, float(price),
                                                                                       int(qty),
                                                                                       delay=0)
            fix_manager.send_message_fix_standard(fix_message)
            order_id_first = order_book.extract_field(OrderBookColumns.order_id.value)
            fix_manager.send_message_fix_standard(fix_message)
            order_id_second = order_book.extract_field(OrderBookColumns.order_id.value)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion
        #
        # region massbook
        order_book.mass_book([1, 2])
        time.sleep(5)
        # # endregion
        #
        # # region mass approve
        middle_office.mass_approve([1, 2])
        # endregion

        # region  verify values after massbook
        values_of_first_block = middle_office.extract_list_of_block_fields([extract_sts, extract_sts_match_status,
                                                                            block_id],
                                                                           row_number=1)
        values_of_second_block = middle_office.extract_list_of_block_fields([extract_sts, extract_sts_match_status,
                                                                             block_id],
                                                                            row_number=2)
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched', block_id: '*'},
                                     values_of_first_block, "Compare Block 1")
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched', block_id: '*'},
                                     values_of_second_block, "Compare Block 2")
        # endregion

        # region mass_allocate
        middle_office.mass_allocate([1, 2])
        values_of_first_block_allocate = middle_office.extract_list_of_block_fields(
            [extract_sts, extract_sts_match_status,
             extract_summary_status],
            row_number=1)
        values_of_second_block_allocate = middle_office.extract_list_of_block_fields(
            [extract_sts, extract_sts_match_status,
             extract_summary_status],
            row_number=2)
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched',
                                      extract_summary_status: 'MatchedAgreed'},
                                     values_of_first_block_allocate, "Compare Block 1")
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched',
                                      extract_summary_status: 'MatchedAgreed'},
                                     values_of_second_block_allocate, "Compare Block 2")
        status_1 = middle_office.extract_allocate_value(extract_sts)
        match_status_1 = middle_office.extract_allocate_value(extract_sts_match_status)
        alloc_id_1 = middle_office.extract_allocate_value(AllocationsColumns.alloc_id.value)
        middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'}, status_1,
                                     'Status 2 allocation record', )
        middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, match_status_1,
                                     'Match Status 2 allocation record')
        middle_office.compare_values({AllocationsColumns.alloc_id.value: '*'}, alloc_id_1,
                                     'Allocation 2 allocation record')

        #  region FALSE WITHDRAWAL
        middle_office.extract_list_of_block_fields([extract_sts],
                                                   filter_list=[block_id,
                                                                values_of_second_block[
                                                                    block_id]])
        # endregion
        status_2 = middle_office.extract_allocate_value(AllocationsColumns.sts.value)
        match_status_2 = middle_office.extract_allocate_value(AllocationsColumns.match_status.value)
        alloc_id_2 = middle_office.extract_allocate_value(AllocationsColumns.alloc_id.value)
        middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'}, status_2,
                                     'Status 2 allocation record', )
        middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, match_status_2,
                                     'Match Status 2 allocation record')
        middle_office.compare_values({AllocationsColumns.alloc_id.value: '*'}, alloc_id_2,
                                     'Allocation 2 allocation record')
        #  region FALSE WITHDRAWAL
        middle_office.extract_list_of_block_fields([extract_sts],
                                                   filter_list=[extract_sts,
                                                                values_of_second_block[
                                                                    extract_sts]])
        # endregion

        # region unallocate
        middle_office.mass_unallocate([1, 2])
        # endregion

        # region extracting verifying of values
        values_of_first_block_unallocate = middle_office.extract_list_of_block_fields(
            [extract_sts, extract_sts_match_status,
             extract_summary_status],
            row_number=1)
        values_of_second_block_unallocate = middle_office.extract_list_of_block_fields(
            [extract_sts, extract_sts_match_status,
             extract_summary_status],
            row_number=2)
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched',
                                      extract_summary_status: ''},
                                     values_of_first_block_unallocate, "Compare Block 1")
        middle_office.compare_values({extract_sts: 'Accepted', extract_sts_match_status: 'Matched',
                                      extract_summary_status: ''},
                                     values_of_second_block_unallocate, "Compare Block 2")

        status_1_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.sts.value)
        match_status_1_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.match_status.value)
        alloc_id_1_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.alloc_id.value)
        middle_office.compare_values({AllocationsColumns.sts.value: 'Canceled'}, status_1_after_unallocated,
                                     'Status 2 allocation record (after unallocated)', )
        middle_office.compare_values({AllocationsColumns.match_status.value: 'Unmatched'},
                                     match_status_1_after_unallocated,
                                     'Match Status 2 allocation record (after unallocated)')
        middle_office.compare_values({AllocationsColumns.alloc_id.value: '*'}, alloc_id_1_after_unallocated,
                                     'Allocation 2 allocation record (after unallocated)')

        #  region FALSE WITHDRAWAL
        middle_office.extract_list_of_block_fields([extract_sts],
                                                   filter_list=[block_id,
                                                                values_of_second_block[
                                                                    block_id]])
        # endregion

        status_2_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.sts.value)
        match_status_2_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.match_status.value)
        alloc_id_2_after_unallocated = middle_office.extract_allocate_value(AllocationsColumns.alloc_id.value)
        middle_office.compare_values({AllocationsColumns.sts.value: 'Canceled'}, status_2_after_unallocated,
                                     'Status 2 allocation record (after unallocated)', )
        middle_office.compare_values({AllocationsColumns.match_status.value: 'Unmatched'},
                                     match_status_2_after_unallocated,
                                     'Match Status 2 allocation record (after unallocated)')
        middle_office.compare_values({AllocationsColumns.alloc_id.value: '*'}, alloc_id_2_after_unallocated,
                                     'Allocation 2 allocation record (after unallocated)')
        # endregion
