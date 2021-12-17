import logging
import os

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_5728(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity
        self.wa_connectivity = SessionAliasOMS().wa_connectivity

    def qap_5728(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        client = 'CLIENT_COMM_1'
        change_params = {'Account': client,
                         "Instrument": Instrument.ISI1.value,
                         "ExDestination": "XEUR",
                         'PreAllocGrp': {
                             'NoAllocs': [{
                                 'AllocAccount': "CLIENT_COMM_1_SA2",
                                 'AllocQty': "100"}]}}
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit().change_parameters(change_params)
        fix_verifier = FixVerifier(self.dc_connectivity, self.case_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        fee_commission = RestCommissionsSender(self.wa_connectivity, self.case_id)
        fee_commission.send_default_fee()
        fee_commission.modify_client_commission_request()
        fee_commission.send_post_request()
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
        middle_office.book_order()
        # endregion
        # region approve block
        middle_office.approve_block()
        # endregion

        # region allocate
        middle_office.allocate_block()
        # endregion

        # region verify Confirmation message
        fix_response_confirmation = FixMessageConfirmationReportOMS().set_default_confirmation_new(fix_message)
        fix_response_confirmation.change_parameters({'SettlCurrFxRate': '*',
                                                     'NoMiscFees': [{
                                                         'MiscFeeAmt': '*',
                                                         'MiscFeeCurr': '*',
                                                         'MiscFeeType': '*'
                                                     }],
                                                     'CommissionData': {
                                                         'CommissionType': '*',
                                                         'Commission': '*',
                                                         'CommCurrency': '*'
                                                     }
                                                     })
        fix_verifier.check_fix_message_fix_standard(fix_response_confirmation)
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5728()
