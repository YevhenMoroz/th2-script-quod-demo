import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards \
    import ValuesTab, DimensionsTab, MainWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3272(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instrument_type = 'Bond'
        self.trading_phase = 'Open'
        self.route = self.data_set.get_route("route_1")
        self.execution_policy = 'Care'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_risk_limit_dimension_page()
            time.sleep(2)
            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name)
            time.sleep(2)

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_instrument_type(self.instrument_type)
            dimensions_tab.set_trading_phase(self.trading_phase)
            dimensions_tab.set_route(self.route)
            dimensions_tab.set_execution_policy(self.execution_policy)

            wizard = MainWizard(self.web_driver_container)
            time.sleep(2)
            self.verify("Info message \"Maximum 4 different dimensions\" appears", True,
                        wizard.is_dimensions_limit_info_message_appears())

            excepted_result = ["Accounts dimensions: False", "Users dimension: False", "Reference data dimension: False",
                               "Instrument Type: True", "Trading Phase: True", "Route: True", "Execution Policy: True",
                               "Position Type: False", "Position Validity: False", "Settlement Period: False",
                               "Side: False"]
            actual_result = [f"Accounts dimensions: {dimensions_tab.is_accounts_dimension_enabled()}",
                             f"Users dimension: {dimensions_tab.is_users_dimension_enabled()}",
                             f"Reference data dimension: {dimensions_tab.is_reference_data_enabled()}",
                             f"Instrument Type: {dimensions_tab.is_instrument_type_enabled()}",
                             f"Trading Phase: {dimensions_tab.is_trading_phase_enabled()}",
                             f"Route: {dimensions_tab.is_route_enabled()}",
                             f"Execution Policy: {dimensions_tab.is_execution_policy_enabled()}",
                             f"Position Type: {dimensions_tab.is_position_type_enabled()}",
                             f"Position Validity: {dimensions_tab.is_position_type_enabled()}",
                             f"Settlement Period: {dimensions_tab.is_settlement_period_enabled()}",
                             f"Side: {dimensions_tab.is_side_enabled()}"]
            self.verify("Unfilled fields in Dimensions became disabled", excepted_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
