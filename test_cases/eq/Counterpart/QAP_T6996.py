import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiSettlementModelMessages import RestApiSettlementModelMessages
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6996(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_conn = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_conn, case_id=self.case_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.case_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        filter_list = [OrderBookColumns.cl_ord_id.value, self.fix_message.get_parameter('ClOrdID')]
        self.fix_message.change_parameter("HandlInst", '3')

        # region precondition and step 1
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        vanue_id = self.data_set.get_venue_id('paris')
        api_message = RestApiSettlementModelMessages(self.data_set)
        api_message.set_modify_message_amend(client, venue_id=vanue_id)
        self.rest_api_manager.send_post_request(api_message)
        self.fix_manager.send_message_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        fix_execution_report.set_default_new(self.fix_message)
        fix_execution_report.remove_parameter("Parties").add_tag({'QuodTradeQualifier': '*'})
        fix_execution_report.add_tag({'BookID': '*'}).add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'})
        fix_execution_report.add_tag({"NoParty": {'NoParty': [
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': '10',
             'PartyID': "CREST",
             'PartyIDSource': "D"}]}})
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report)
        self.order_book.manual_execution(qty, price=price)
        self.order_book.set_filter(filter_list=filter_list)
        exec_sts = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value})
        self.order_book.compare_values({OrderBookColumns.exec_sts.value: ExecSts.filled.value}, exec_sts,
                                       f"Comparing {OrderBookColumns.exec_sts.value} of order")
        # endregion

        # region step 2
        fix_execution_report.set_default_filled(self.fix_message)
        fix_execution_report.remove_parameter("Parties").add_tag({'QuodTradeQualifier': '*'}). \
            remove_parameter('SettlCurrency').remove_parameter('LastExecutionPolicy'). \
            remove_parameter('TradeReportingIndicator').add_tag({'VenueType': '0'}).remove_parameter('SecondaryExecID') \
            .remove_parameter('SecondaryOrderID').add_tag({'LastMkt': '*'}).change_parameter('VenueType', 'O')
        fix_execution_report.add_tag({'BookID': '*'}).add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'})
        fix_execution_report.add_tag({"NoParty": {'NoParty': [
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': '10',
             'PartyID': "CREST",
             'PartyIDSource': "D"}]}})
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report)
        api_message.set_modify_message_clear()
        self.rest_api_manager.send_post_request(api_message)
        # endregion
