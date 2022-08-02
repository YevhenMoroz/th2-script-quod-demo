import logging

from pathlib import Path
from custom.basic_custom_actions import create_event
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7173(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = create_event(self.__class__.__name__, self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.change_params = {'Account': self.client,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.client_acc,
                                      'AllocQty': "100"}]}}
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit().change_parameters(
            self.change_params)
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.case_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.send_default_fee()
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region manual execute CO order
        self.order_book.manual_execution()
        # endregion
        # region complete CO order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        # endregion
        # region Book order
        self.mid_office.book_order()
        # endregion
        # region approve block
        self.mid_office.approve_block()
        # endregion
        # region allocate
        self.mid_office.allocate_block()
        # endregion
        # region verify Confirmation message
        fix_response_confirmation = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        no_mics = {
                "MiscFeeAmt": "*", "MiscFeeCurr": "*", "MiscFeeType": "*"}
        fix_response_confirmation.change_parameters(
            {'tag5120': "*", "AllocQty": self.qty, "AllocAccount": self.client_acc, "Account": self.client,
             "CommissionData": {"CommissionType": "*", "Commission": "*", "CommCurrency": "*"}, 'NoMiscFees': no_mics})
        self.fix_verifier_dc.check_fix_message_fix_standard(fix_response_confirmation)
        # endregion
