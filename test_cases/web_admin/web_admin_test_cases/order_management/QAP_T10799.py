import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10799(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.strategy_type = self.data_set.get_strategy_type("strategy_type_1")
        self.price_offset_type = ['Ticks', 'FxPipPrecision', 'Percentage', 'BasisPoints']
        self.price_offset_value = ['10', '-10', '0']
        self.price_reference = ['Manual', 'RelatedToMarketPrice', 'RelatedToPrimaryPrice', 'RelatedToMidpointPrice', 'RelatedToLastTradePrice',
                                'RelatedToOpenPrice', 'RelatedToClosePrice', 'RelatedToHighPrice', 'RelatedToLowPrice']
        self.ord_type = ['AtAuction', 'AtAuctionLimit', 'EnhancedLimitOrder', 'Limit', 'Market', 'MarketLeftOverLimit', 'MarketLeftOverRef',
                         'NotSpecified', 'OnClose', 'Pegged', 'PreviouslyIndicated', 'PreviouslyQuoted', 'SpecialLimitOrder', 'Stop', 'StopLimit']
        self.tif = ['AtCrossing', 'AtTheClose', 'AtTheOpening', 'Day', 'FillOrKill', 'GoodForVWAPCrossing', 'GoodTillCancel', 'GoodTillCrossing',
                    'GoodTillDate', 'ImmediateOrCancel', 'TradeAtLast', 'ValidForAuction']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_execution_strategies_page()
        side_menu.wait_for_button_to_become_active()

    def test_context(self):
        try:
            self.precondition()

            main_page = ExecutionStrategiesPage(self.web_driver_container)
            main_page.click_on_new_button()
            strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            for offset_type in self.price_offset_type:
                strategies_wizard.set_price_offset_type(offset_type)
            for price_offset_value in self.price_offset_value:
                strategies_wizard.set_price_offset_value(price_offset_value)
            for price_reference in self.price_reference:
                strategies_wizard.set_price_reference(price_reference)
            for tif in self.tif:
                strategies_wizard.set_tif(tif)
            for ord_type in self.ord_type:
                strategies_wizard.set_ord_type(ord_type)

            self.verify("All the Offset parameters are present", True, True)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            basic_custom_actions.create_event("TEST FAILED", self.test_case_id,
                                              'FAILED', f'{traceback.extract_tb(exc_traceback, limit=2)}, {sys.stdout}')
            print(" Search in ->  " + self.__class__.__name__)
