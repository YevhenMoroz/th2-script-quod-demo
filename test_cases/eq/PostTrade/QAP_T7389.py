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
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7389(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        first_alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        second_alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_2')
        no_allocs: dict = {'NoAllocs': [
            {
                'AllocAccount': first_alloc_account,
                'AllocQty': str(int(int(qty) / 2))
            },
            {
                'AllocAccount': second_alloc_account,
                'AllocQty': str(int(int(qty) / 2))
            }
        ]}
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion

        # region step 1
        self.middle_office.book_order()
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        status = self.middle_office.extract_block_field(MiddleOfficeColumns.sts.value,
                                                        filter_list=[MiddleOfficeColumns.block_id.value,
                                                                     block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'ApprovalPending'}, status,
                                          'Comparing status after book')
        # endregion

        # region step 2
        self.middle_office.approve_block()
        status = self.middle_office.extract_block_field(MiddleOfficeColumns.sts.value,
                                                        filter_list=[MiddleOfficeColumns.block_id.value,
                                                                     block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'Accepted'}, status,
                                          'Comparing status after book')
        # endregion

        # region step 3
        fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_message.set_default_confirmation_new(self.fix_message)
        confirmation_message.change_parameter('AllocAccount', first_alloc_account).change_parameter('Account', '*'). \
            change_parameter('AllocQty', str(int(int(qty) / 2))).change_parameter('SettlCurrFxRate',
                                                                                  '*').change_parameter('tag5120', '*')
        self.middle_office.allocate_block()
        fix_verifier.check_fix_message_fix_standard(confirmation_message,
                                                    ['ConfirmTransType', 'NoOrders', 'AllocAccount'])
        confirmation_message.change_parameter('AllocAccount', second_alloc_account)
        fix_verifier.check_fix_message_fix_standard(confirmation_message,
                                                    ['ConfirmTransType', 'NoOrders', 'AllocAccount'])
