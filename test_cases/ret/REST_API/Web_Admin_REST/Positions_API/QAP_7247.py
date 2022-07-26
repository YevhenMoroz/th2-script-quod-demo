import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import RestApiCashAccountMessages
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager


class QAP_7247(TestCase):
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
        self.buying_power_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=data_set)
        self.security_account_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        self.cash_account_message = RestApiCashAccountMessages(data_set=data_set)
        self.tested_security_account = self.data_set.get_account_by_name('account_4')
        self.tested_cash_account_currency = self.data_set.get_currency_by_name('currency_2')
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name('instrument_3')
        self.tested_instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_3')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        pass