import logging
import os

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_7167(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity

    def qap_5753(self):
        # region Declaration
        order_book = OMSOrderBook(self.test_id, self.session_id)
        base_window = BaseMainWindow(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        fix_manager = FixManager(self.ss_connectivity, self.test_id)
        security_account = 'MOClient_SA1'
        client = 'MOClient'
        change_params = {'Account': client,
                         'PreAllocGrp': {
                             'NoAllocs': [{
                                 'AllocAccount': "MOClient_SA1",
                                 'AllocQty': "100"}]}}
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit().change_parameters(change_params)
        fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        CHECKED_VALUE = '42000'
        middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion

        # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        order_book.scroll_order_book(1)
        order_id = order_book.extract_field('Order ID')
        # endregion

        # region accept CO order
        client_inbox.accept_order('O', 'M', 'S')
        # endregion

        # region manual execute CO order
        order_book.manual_execution(fix_message.get_parameter('OrderQtyData')['OrderQty'])
        # endregion

        # region complete CO order
        order_book.complete_order(filter_list=['Order ID', order_id])
        # endregion

        # region Book order
        middle_office.set_modify_ticket_details(settl_currency='UAH', exchange_rate='2', exchange_rate_calc='Multiply',
                                                extract_book=True)
        middle_office.book_order()
        # endregion

        # region verify AllocationInstruction message
        fix_report_allocinstr = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(fix_message)
        fix_report_allocinstr.add_tag(
            {'RootSettlCurrency': '*', 'RootSettlCurrFxRateCalc': '*', 'RootSettlCurrAmt': '*',
             'RootSettlCurrAmt': CHECKED_VALUE, 'RootSettlCurrFxRate': '*'})
        fix_verifier.check_fix_message_fix_standard(fix_report_allocinstr)

        # endregion

        # region approve block
        middle_office.approve_block()
        # endregion

        # region allocate
        middle_office.allocate_block()
        # endregion

        # region verify second allocation instruction
        fix_report_allocinstr.set_default_preliminary(fix_message).remove_parameter(
            'NoAllocs').change_parameters({'NoAllocs', [
            {'AllocSettlCurrAmt': '*', 'AllocSettlCurrency': '*', 'SettlCurrAmt': '*', 'SettlCurrFxRate': '*',
             'SettlCurrency': '*', 'SettlCurrFxRateCalc': '*', 'AllocQty': '*',
             'AllocNetPrice': '*', 'AllocAccount': '*', 'AllocPrice': '*'}]})
        fix_verifier.check_fix_message_fix_standard(fix_report_allocinstr)
        # endregion

        # region verify Confirmation message
        fix_response_confirmation = FixMessageConfirmationReportOMS().set_default_confirmation_new(fix_message)
        fix_response_confirmation.add_tag(
            {'SettlCurrFxRate': '*', 'SettlCurrFxRateCalc': '*', 'SettlCurrency': '*', 'SettlCurrAmt': CHECKED_VALUE})
        fix_verifier.check_fix_message_fix_standard(fix_response_confirmation)
        # endregion

    @try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5753()
