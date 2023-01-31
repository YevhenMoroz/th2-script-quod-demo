import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7223(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '1000'
        self.price = '10'
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.client = self.data_set.get_client('client_counterpart_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.firm_client = self.data_set.get_client_by_name('client_pos_3')
        self.firm_acount = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order (precondition)
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region do house fill (step 1)
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry_message.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'SourceAccountID': self.firm_acount})
        self.java_api_manager.send_message(self.trade_entry_message)
        # endregion

        # region check fix message (step 2)
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_filled(self.fix_message)
        execution_report.remove_parameter('Parties').remove_parameter('SettlCurrency'). \
            remove_parameter('LastExecutionPolicy').remove_parameter('TradeReportingIndicator'). \
            remove_parameter('SecondaryOrderID').remove_parameter('SecondaryExecID')
        execution_report.change_parameters({'QuodTradeQualifier': '*',
                                            'BookID': '*',
                                            'NoParty': '*',
                                            'tag5120': '*',
                                            'LastMkt': '*',
                                            'ExecBroker': '*',
                                            'VenueType': '*',
                                            })
        list_of_ignored_fields = ['NoParty', 'SecurityDesc', 'GatingRuleCondName', 'GatingRuleName']
        execution_report.change_parameters({'Side': '1'})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ['ClOrdID', 'OrdStatus', 'Side'], ignored_fields=list_of_ignored_fields)
        execution_report.change_parameters({'Side': '2', 'Account': self.firm_client})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ['ClOrdID', 'OrdStatus', 'Side'], ignored_fields=list_of_ignored_fields)
        # endregion
