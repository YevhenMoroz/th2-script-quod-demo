import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.trading_api.ApiMessageMarketQuoteRequest import ApiMessageMarketQuoteRequest
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3195(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.buying_power_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=data_set)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.market_quote_message = ApiMessageMarketQuoteRequest(data_set=data_set)
        self.tested_instrument_tcs_iq = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        self.tested_instrument_spicejet_iq = self.data_set.get_trading_api_instrument_by_name('instrument_5')
        self.bid_tcs_iq = 0
        self.ask_spicejet_iq = 0

    @staticmethod
    def check_md_entry_px(market_quote_response, md_entry_type, test_id):
        for count in range(len(market_quote_response)):
            market_data_fulls = market_quote_response[count].keys()
            if 'MDEntryType' in market_data_fulls and market_quote_response[count]['MDEntryType'] == md_entry_type:
                bca.create_event(f'{md_entry_type} for instrument was found', status='SUCCESS', parent_id=test_id)
                return market_quote_response[count]['MDEntryPx']
        bca.create_event(f'{md_entry_type} for instrument was not found', status='FAILED',
                         parent_id=test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region, Check that Gross Order Value is calculated correctly with, OrderType=Market side=Sell and Bid value

        # TCS-IQ
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=50)
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)

        self.market_quote_message.tested_instrument_mq = self.tested_instrument_tcs_iq
        self.market_quote_message.set_default_request()
        market_quote_response_bid = self.trd_api_manager.parse_response_details_repeating_group(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.market_quote_message))
        try:
            self.bid_tcs_iq = self.check_md_entry_px(market_quote_response_bid, 'Bid', self.test_id)
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)

        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.noss_message.change_parameter(parameter_name='OrdType', new_parameter_value='Market')
        self.noss_message.remove_parameter(parameter_name='Price')
        noss_response_sell = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        gross_order_value = self.buying_power_manager.calc_gross_order_value(self.test_id,
                                                                             noss_response_sell,
                                                                             reference_price=self.bid_tcs_iq)
        data_validation(test_id=self.test_id,
                        event_name="Check that Gross Order Value is calculated correctly with OrderType=Market, "
                                   "side=Sell and Bid value",
                        expected_result=gross_order_value,
                        actual_result=float(noss_response_sell['GrossOrdAmt']))
        # endregion

        # region, Check that Gross Order Value is calculated correctly with OrderType=Market, side=Buy and ASK value

        # SPICEJET-IQ
        self.nos_message.default_instrument_nos = self.tested_instrument_spicejet_iq
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=40)
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)

        self.market_quote_message.tested_instrument_mq = self.tested_instrument_spicejet_iq
        self.market_quote_message.set_default_request()

        market_quote_response_ask = self.trd_api_manager.parse_response_details_repeating_group(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.market_quote_message))
        try:
            self.ask_spicejet_iq = self.check_md_entry_px(market_quote_response_ask, 'Offer', self.test_id)
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)

        self.noss_message.default_instrument_noss = self.tested_instrument_spicejet_iq
        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='OrdType', new_parameter_value='Market')
        self.noss_message.remove_parameter(parameter_name='Price')
        noss_response_buy = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        gross_order_value_buy = self.buying_power_manager.calc_gross_order_value(self.test_id,
                                                                                 noss_response_buy,
                                                                                 reference_price=self.ask_spicejet_iq)
        data_validation(test_id=self.test_id,
                        event_name="Check that Gross Order Value is calculated correctly with OrderType=Market, side=Buy "
                                   "and Ask value",
                        expected_result=gross_order_value_buy,
                        actual_result=float(noss_response_buy['GrossOrdAmt']))
        # endregion

        # region, Check that Gross Order Value is calculated correctly with OrderType=Limit and side=Buy
        self.noss_message.set_default_request()
        noss_response_limit = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        data_validation(test_id=self.test_id,
                        event_name="Check that Gross Order Value is calculated correctly with OrderType=Limit",
                        expected_result=float(self.noss_message.parameters['Price']),
                        actual_result=float(noss_response_limit['GrossOrdAmt']))
        # endregion

