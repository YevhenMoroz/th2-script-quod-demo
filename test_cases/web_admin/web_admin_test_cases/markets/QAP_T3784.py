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


class QAP_T3784(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.test_data = {"name": "QAP4184",
                          "venue":
                              {"id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                               "type": "DarkPool",
                               "client_venue_id": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))},
                          "subvenue":
                              {"venue": "AMEX"}}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        time.sleep(2)
        venues_page = VenuesPage(self.web_driver_container)
        venues_page.set_name_filter(self.test_data["name"])
        time.sleep(1)
        if not venues_page.is_searched_venue_found(self.test_data["name"]):
            venues_page.click_on_new()
            time.sleep(2)
            venues_values_wizard = VenuesValuesSubWizard(self.web_driver_container)
            venues_values_wizard.set_name(self.test_data["name"])
            venues_values_wizard.set_id(self.test_data["venue"]["id"])
            venues_values_wizard.set_type(self.test_data["venue"]["type"])
            venues_values_wizard.set_client_venue_id(self.test_data["venue"]["client_venue_id"])
            venues_wizard = VenuesWizard(self.web_driver_container)
            venues_wizard.click_on_save_changes()
            time.sleep(2)

        side_menu.open_subvenues_page()
        time.sleep(2)
        subvenue_page = SubVenuesPage(self.web_driver_container)
        subvenue_page.set_name_filter(self.test_data["name"])
        time.sleep(1)
        if not subvenue_page.is_searched_subvenue_found(self.test_data["name"]):
            subvenue_page.click_on_new()
            time.sleep(2)
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
            time.sleep(2)
            venues_page = VenuesPage(self.web_driver_container)
            venues_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            venues_page.click_on_more_actions()
            time.sleep(1)
            venues_page.click_on_edit()
            time.sleep(2)
            venues_values_wizard = VenuesValuesSubWizard(self.web_driver_container)
            selected_values_at_position_flattening_period = \
                [str(i).strip() for i in venues_values_wizard.get_position_flattening_period().split(",")]
            if len(selected_values_at_position_flattening_period) > 1:
                venues_values_wizard.set_position_flattening_period(selected_values_at_position_flattening_period)
            venues_wizard = VenuesWizard(self.web_driver_container)
            venues_wizard.click_on_save_changes()
            time.sleep(2)
            venues_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            self.verify("Venue has been saved with the empty Position Flattering Period field", True,
                        venues_page.is_searched_venue_found(self.test_data["name"]))

            side_menu.open_subvenues_page()
            time.sleep(2)
            subvenue_page = SubVenuesPage(self.web_driver_container)
            subvenue_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            subvenue_page.click_on_more_actions()
            time.sleep(1)
            subvenue_page.click_on_edit()
            time.sleep(2)
            subvenue_description_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
            selected_values_at_position_flattening_period = \
                [str(i).strip() for i in subvenue_description_wizard.get_position_flattening_period().split(",")]
            if "" not in selected_values_at_position_flattening_period:
                subvenue_description_wizard.set_position_flattening_period(
                    selected_values_at_position_flattening_period)
            subvenue_wizard = SubVenuesWizard(self.web_driver_container)
            subvenue_wizard.click_on_save_changes()
            time.sleep(2)
            subvenue_page.set_name_filter(self.test_data["name"])
            time.sleep(1)
            self.verify("SubVenue has been saved with the empty Position Flattering Period field", True,
                        subvenue_page.is_searched_subvenue_found(self.test_data["name"]))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
