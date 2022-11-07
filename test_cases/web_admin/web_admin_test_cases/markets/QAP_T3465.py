import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_description_sub_wizard \
    import SubVenuesDescriptionSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3465(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_venues_page()
            time.sleep(2)
            venue_page = VenuesPage(self.web_driver_container)
            venue_page.click_on_new()
            time.sleep(2)
            venue_values_tab = VenuesValuesSubWizard(self.web_driver_container)
            self.verify("All checkboxes selected in Venue creation wizard", True,
                        venue_values_tab.is_all_position_flattening_period_entity_selected())

            side_menu.open_subvenues_page()
            time.sleep(2)
            sub_venue_page = SubVenuesPage(self.web_driver_container)
            sub_venue_page.click_on_new()
            time.sleep(2)
            sub_venue_description_tab = SubVenuesDescriptionSubWizard(self.web_driver_container)
            self.verify("All checkboxes selected in SubVenue creation wizard", True,
                        sub_venue_description_tab.is_all_position_flattening_period_entity_selected())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
