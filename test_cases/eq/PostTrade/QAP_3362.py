import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_3362(TestCase):
    def __init__(self, report_id, session_id, data_set):
        super().__init__(report_id, session_id, data_set)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.fix_manager = FixManager(ss_connectivity)
        self.qty = '300'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_8'))
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.price = self.fix_message.get_parameter('Price')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        order_id_first = None
        # region create  DMA order
        try:
            rule_manager = RuleManager(Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(bs_connectivity,
                                                                                       self.client_for_rule,
                                                                                       self.exec_destination,
                                                                                       float(self.price),
                                                                                       int(self.qty),
                                                                                       delay=0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
            order_id_first = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # except Exception as e:
        #     # logger.error(f'{e}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion
        # region split book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        split_param_1 = self.order_book.create_split_booking_parameter("100")
        split_param_2 = self.order_book.create_split_booking_parameter('200')
        self.order_book.split_book([split_param_1, split_param_2])
        #
        # # endregion
        #
        # # region mass_approve
        self.middle_office.mass_approve([1, 2])

        self.__verify_after_mass_action_for_block(2, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value
                                                      ],
                                                  'approve', {MiddleOfficeColumns.sts.value: 'Accepted',
                                                              MiddleOfficeColumns.match_status.value: 'Matched'})
        self.__verify_after_mass_action_for_block(1, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value
                                                      ]
                                                  , 'approve', {MiddleOfficeColumns.sts.value: 'Accepted',
                                                                MiddleOfficeColumns.match_status.value: 'Matched'})
        # endregion

        # region mass_allocate
        self.middle_office.mass_allocate([1, 2])
        self.__verify_after_mass_action_for_block(2, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value,
                                                      MiddleOfficeColumns.summary_status.value],
                                                  'allocate', {MiddleOfficeColumns.sts.value: 'Accepted',
                                                               MiddleOfficeColumns.match_status.value: 'Matched',
                                                               MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'
                                                               })
        self.__verify_after_mass_action_for_block(1, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value,
                                                      MiddleOfficeColumns.summary_status.value]
                                                  , 'allocate', {MiddleOfficeColumns.sts.value: 'Accepted',
                                                                 MiddleOfficeColumns.match_status.value: 'Matched',
                                                                 MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'
                                                                 })
        #  region FALSE WITHDRAWAL
        self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value],
                                                        filter_list=[MiddleOfficeColumns.qty.value, '100'])
        # endregion
        # endregion
        status_allocation = self.middle_office.extract_allocate_value(AllocationsColumns.sts.value, order_number=1)
        watch_status = self.middle_office.extract_allocate_value(AllocationsColumns.match_status.value, order_number=1)
        self.middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'},
                                          status_allocation,
                                          'Allocation 1 after mass_allocate')
        self.middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, watch_status,
                                          'Allocation 1 after mass_allocate')

        self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value],
                                                        filter_list=[MiddleOfficeColumns.qty.value, '200'])

        status_allocation = self.middle_office.extract_allocate_value(AllocationsColumns.sts.value, order_number=1)
        self.middle_office.clear_filter()
        watch_status = self.middle_office.extract_allocate_value(AllocationsColumns.match_status.value, order_number=1)
        self.middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'},
                                          status_allocation,
                                          'Allocation 2 after mass_allocate')
        self.middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, watch_status,
                                          'Allocation 2 after mass_allocate')

        # endregion

        # region try unbook order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        self.order_book.extract_field(OrderBookColumns.qty.value)
        self.middle_office.un_book_order()
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                       {OrderBookColumns.post_trade_status.value: post_trade_status},
                                       'Compare incorrect unbook')
        # endregion

        # region unallocate
        self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value],
                                                        filter_list=[MiddleOfficeColumns.sts.value,
                                                                     'Accepted'])
        self.middle_office.mass_unallocate([1, 2])
        # region

        # region unBook order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        self.order_book.extract_field(OrderBookColumns.qty.value)
        self.middle_office.un_book_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'ReadyToBook'},
                                       {OrderBookColumns.post_trade_status.value: post_trade_status},
                                       'Compare incorrect UnBook')

        # endregion

    def __verify_after_mass_action_for_block(self, row_number: int, list_of_column: list, after_action: str,
                                             dict_of_expected_result: dict):
        value_for_first_row = self.middle_office.extract_list_of_block_fields(list_of_column,
                                                                              row_number=row_number)
        self.middle_office.compare_values(dict_of_expected_result, value_for_first_row,
                                          f'Checked {row_number} row block after {after_action}')
