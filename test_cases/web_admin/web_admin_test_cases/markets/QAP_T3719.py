import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard \
    import VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3719(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.test_data = "aaaaaaaaaaaaaaaaa"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            values_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
            values_sub_wizard.set_country_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Country if the entered data is not valid", "Not found",
                        values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            values_sub_wizard.set_counterpart_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Counterpart if the entered data is not valid", "Not found",
                        values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            profiles_sub_wizard = VenuesProfilesSubWizard(self.web_driver_container)
            profiles_sub_wizard.set_price_limit_profile_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Price Limit Profile if the entered data is not valid", "Not found",
                        values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            profiles_sub_wizard.set_tick_size_profile_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Tick Size Profile if the entered data is not valid", "Not found",
                        values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            profiles_sub_wizard.set_trading_phase_profile_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Trading Phase Profile if the entered data is not valid",
                        "Not found", values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            profiles_sub_wizard.set_routing_param_group_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Routing Param Group if the entered data is not valid",
                        "Not found", values_sub_wizard.is_not_found_present_in_drop_menu())
            time.sleep(1)
            profiles_sub_wizard.set_holiday_custom_value(self.test_data)
            self.verify("Displays 'Not Found' in the Holiday if the entered data is not valid",
                        "Not found", values_sub_wizard.is_not_found_present_in_drop_menu())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
