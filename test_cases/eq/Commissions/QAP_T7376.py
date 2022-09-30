import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import TradeBookColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7376(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "4373"
        self.price = "4373"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.trades = OMSTradesBook(self.test_id, self.session_id)

        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id,
                                                            self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_fees_message(fee_type=self.data_set.get_misc_fee_type_by_name("agent"))
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_2"),
                                                           "contraFirmCounterpartID": self.data_set.get_counterpart_id(
                                                               "contra_firm")})
        self.rest_commission_sender.send_post_request()
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        self.client_inbox.accept_order(filter=filter_dict)
        self.order_book.manual_execution(filter_dict=filter_dict,
                                         contra_firm=self.data_set.get_counterpart("counterpart_cnf_1"))
        self.__verify_commissions()

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(
            "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2"),
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)

    @try_except(test_id=Path(__file__).name[:-3])
    def __verify_commissions(self):
        order_id = self.response[0].get_parameter("OrderID")
        self.trades.set_filter([TradeBookColumns.order_id.value, order_id, TradeBookColumns.exec_type.value, "Trade"])
        fees = {TradeBookColumns.exec_fees.value: self.trades.extract_field(TradeBookColumns.exec_fees.value)}
        self.trades.compare_values({TradeBookColumns.exec_fees.value: "0.01"}, fees, event_name='Check values')
