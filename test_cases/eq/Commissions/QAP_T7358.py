import logging
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
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import AllocationsColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7358(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "150"
        self.price = "20"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit(
            "instrument_3").change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             "ExDestination": self.data_set.get_mic_by_name("mic_2"),
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameters(
            {'Account': self.client, "OrderQtyData": {'OrderQty': self.qty}, "Price": self.price})
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.trades = OMSTradesBook(self.case_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.case_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_fees_message(fee=self.data_set.get_fee_by_name('fee_vat'),
                                                            recalculate=True,
                                                            fee_type=self.data_set.get_misc_fee_type_by_name(
                                                                'value_added_tax'))
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_2"),
                                                           "contraFirmCounterpartID": self.data_set.get_counterpart_id(
                                                               "contra_firm")})
        self.rest_commission_sender.send_post_request()
        # endregion
        # region create order
        self.__send_fix_orders()
        # endregion
        # region approve and allocate block
        ord_id = self.response[0].get_parameters()['OrderID']
        self.mid_office.book_order([OrderBookColumns.order_id.value, ord_id])
        self.mid_office.approve_block()
        allocation_param = [{AllocationsColumns.security_acc.value: self.client_acc,
                             AllocationsColumns.alloc_qty.value: self.qty}]
        self.mid_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.mid_office.allocate_block([OrderBookColumns.order_id.value, ord_id])
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        no_mics = {
            "MiscFeeAmt": "1", "MiscFeeCurr": "*", "MiscFeeType": "22"}
        conf_report.change_parameters({"Account": self.client, "AvgPx": "*", "Currency": "*", "tag5120": "*",
                                       "NoMiscFees": no_mics})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_orders(self):
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)

