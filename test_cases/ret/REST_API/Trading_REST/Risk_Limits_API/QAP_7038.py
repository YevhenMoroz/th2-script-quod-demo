import os
from datetime import datetime, timedelta

from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.web_admin_api.Middle_Office_API.RestApiCommissionProfileMessage import RestApiCommissionProfileMessages


class QAP_7038(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.web_admin = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.web_admin, case_id=self.test_id)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.commission_profile_message = RestApiCommissionProfileMessages(data_set=data_set)
        self.time_now = datetime.utcnow()
        self.listing_description = "TATA CONSULTANCY SERV LTD"
        self.cash_account = "api_cash_account_rin_INR"
        self.venue = "NSE"
        self.expire_date = (self.time_now + timedelta(days=2)).strftime("%Y%m%d")

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region step 2, send requests: findAllCommissionProfile and submitNewOrderSingleSimulate and check result
        self.commission_profile_message.find_all_commission_profile()
        commission_profile = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.commission_profile_message))

        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='ExpireDate',
                                           new_parameter_value=self.expire_date)
        noss_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        try:
            verifier(case_id=self.test_id,
                     event_name="Check that 'Client' value is correct",
                     expected_value=self.noss_message.parameters['ClientAccountGroupID'],
                     actual_value=noss_response['ClientAccountGroupID'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Security Account' value is correct",
                     expected_value=self.noss_message.parameters['PreTradeAllocations'][0]['AllocClientAccountID'],
                     actual_value=noss_response['ClientAccountID'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Listing' value is correct",
                     expected_value=self.noss_message.parameters['Instrument']['InstrSymbol'],
                     actual_value=noss_response['InstrSymbol'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Listing Description' value is correct",
                     expected_value=self.listing_description,
                     actual_value=noss_response['InstrDescription'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Side' value is correct",
                     expected_value=self.noss_message.parameters['Side'],
                     actual_value=noss_response['Side'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Quantity' value is correct",
                     expected_value=float(self.noss_message.parameters['OrdQty']),
                     actual_value=float(noss_response['OrdQty']))
            verifier(case_id=self.test_id,
                     event_name="Check that 'Price' value is correct",
                     expected_value=float(self.noss_message.parameters['Price']),
                     actual_value=float(noss_response['Price']))
            verifier(case_id=self.test_id,
                     event_name="Check that 'Currency' value is correct",
                     expected_value=self.noss_message.parameters['Currency'],
                     actual_value=noss_response['Currency'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Cash Account' value is correct",
                     expected_value=self.cash_account,
                     actual_value=noss_response['ClientCashAccountID'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Venue' value is correct",
                     expected_value=self.venue,
                     actual_value=noss_response['ClientVenueID'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Venue' value is correct",
                     expected_value=self.noss_message.parameters['TimeInForce'],
                     actual_value=noss_response['TimeInForce'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Expire Date' value is correct",
                     expected_value=self.expire_date,
                     actual_value=noss_response['ExpireDate'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'Commission' value is correct",
                     expected_value=commission_profile[0]['commissionPoint'][0]['baseValue'],
                     actual_value=noss_response['BookedClientCommission'])
            verifier(case_id=self.test_id,
                     event_name="Check that 'VAT' value is correct",
                     expected_value=commission_profile[0]['commissionPoint'][0]['baseValue'],
                     actual_value=noss_response['BookedVATMiscFeeAmt'])
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
