import random
import sys
import time
import traceback
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_wizard import SubVenuesWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_description_sub_wizard \
    import SubVenuesDescriptionSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3785(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.test_data = {"name": "QAP4178",
                          "venue":
                              {"id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                               "type": "DarkPool",
                               "client_venue_id": ''.join(
                                   random.sample((string.ascii_uppercase + string.digits) * 6, 6))},
                          "subvenue":
                              {"venue": "QAP4178"}}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        venues_page = VenuesPage(self.web_driver_container)
        venues_page.set_name_filter(self.test_data["name"])
        time.sleep(1)
        if not venues_page.is_searched_venue_found(self.test_data["name"]):
            venues_page.click_on_new()
            venues_values_wizard = VenuesValuesSubWizard(self.web_driver_container)
            venues_values_wizard.set_name(self.test_data["name"])
            venues_values_wizard.set_id(self.test_data["venue"]["id"])
            venues_values_wizard.set_type(self.test_data["venue"]["type"])
            venues_values_wizard.set_client_venue_id(self.test_data["venue"]["client_venue_id"])
            venues_wizard = VenuesWizard(self.web_driver_container)
            venues_wizard.click_on_save_changes()

        side_menu.open_subvenues_page()
        subvenue_page = SubVenuesPage(self.web_driver_container)
        subvenue_page.set_name_filter(self.test_data["name"])
        time.sleep(1)
        if not subvenue_page.is_searched_subvenue_found(self.test_data["name"]):
            subvenue_page.click_on_new()
            subvenue_description_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
            subvenue_description_wizard.set_name(self.test_data["name"])
            subvenue_description_wizard.set_venue(self.test_data["subvenue"]["venue"])
            subvenue_wizard = SubVenuesWizard(self.web_driver_container)
            subvenue_wizard.click_on_save_changes()
            time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_venues_page()
            venues_page = VenuesPage(self.web_driver_container)
            venues_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            venues_page.click_on_more_actions()
            venues_page.click_on_edit()
            venues_values_wizard = VenuesValuesSubWizard(self.web_driver_container)
            venue_all_position_flattening_period = venues_values_wizard.get_all_position_flattening_period_drop_menu()
            venues_values_wizard.set_position_flattening_period(
                random.sample(venue_all_position_flattening_period, int(len(venue_all_position_flattening_period) / 2)))
            venues_values_before_save = [str(i).strip() for i in venues_values_wizard.get_position_flattening_period()
                .split(",")]
            venues_wizard = VenuesWizard(self.web_driver_container)
            venues_wizard.click_on_save_changes()
            venues_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            venues_page.click_on_more_actions()
            venues_page.click_on_edit()
            venues_values_after_save = [str(i).strip() for i in venues_values_wizard.get_position_flattening_period()
                .split(",")]
            self.verify("Venues Position Flattering Period field contains correct date",
                        sorted(venues_values_before_save), sorted(venues_values_after_save))
            venues_wizard.click_on_close()

            side_menu.open_subvenues_page()
            subvenue_page = SubVenuesPage(self.web_driver_container)
            subvenue_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            subvenue_page.click_on_more_actions()
            subvenue_page.click_on_edit()
            subvenue_description_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
            subvenue_venue_all_position_flattening_period = subvenue_description_wizard.get_all_position_flattening_period_drop_menu()
            subvenue_description_wizard.set_position_flattening_period(
                random.sample(subvenue_venue_all_position_flattening_period,
                              int(len(subvenue_venue_all_position_flattening_period) / 2)))
            subvenue_values_before_save = [str(i).strip() for i in subvenue_description_wizard.get_position_flattening_period().split(",")]
            subvenue_wizard = SubVenuesWizard(self.web_driver_container)
            subvenue_wizard.click_on_save_changes()
            subvenue_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            subvenue_page.click_on_more_actions()
            subvenue_page.click_on_edit()
            subvenue_values_after_save = [str(i).strip() for i in subvenue_description_wizard.get_position_flattening_period().split(",")]
            self.verify("SubVenues Position Flattering Period field contains correct date",
                        sorted(subvenue_values_before_save), sorted(subvenue_values_after_save))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
