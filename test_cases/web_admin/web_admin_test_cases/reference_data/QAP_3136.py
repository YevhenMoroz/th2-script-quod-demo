import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.nested_wizards.venues_routing_param_group_sub_wizard import \
    VenuesRoutingParamGroupsSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_profiles_sub_wizard import \
    VenuesProfilesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3136(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "Qwerty123!"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = "15"
        self.type = "DarkPool"
        self.mic = "ALXP"
        self.country = "Albania"
        self.name_at_routing_param_groups = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.negative_routes = ("Direct", "Fixed income Route")
        self.positive_routes = ("Credit Suisse", "JP Morgan")
        self.parameter = "All"
        self.value = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_id(self.id)
        description_sub_wizard.set_type(self.type)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        profiles = VenuesProfilesSubWizard(self.web_driver_container)
        routing_param_groups = VenuesRoutingParamGroupsSubWizard(self.web_driver_container)
        profiles.click_on_routing_param_group()
        time.sleep(2)
        routing_param_groups.click_on_plus_button()
        time.sleep(2)
        routing_param_groups.set_name(self.name_at_routing_param_groups)
        routing_param_groups.click_on_positive_rotes()
        time.sleep(1)
        routing_param_groups.set_positive_routes(self.positive_routes)
        time.sleep(1)
        routing_param_groups.click_on_negative_routes()
        time.sleep(1)
        routing_param_groups.set_negative_routes(self.negative_routes)
        time.sleep(1)
        routing_param_groups.click_on_plus_button_at_parameters()
        time.sleep(2)
        routing_param_groups.set_parameter(self.parameter)
        routing_param_groups.set_value(self.value)
        time.sleep(1)
        routing_param_groups.click_on_checkmark_at_parameters()
        time.sleep(2)
        routing_param_groups.click_on_checkmark()
        time.sleep(2)
        wizard.click_on_go_back_button()

    def test_context(self):
        profiles = VenuesProfilesSubWizard(self.web_driver_container)
        routing_param_groups = VenuesRoutingParamGroupsSubWizard(self.web_driver_container)

        try:
            self.precondition()

            try:
                profiles.set_routing_param_group(self.name_at_routing_param_groups)
                self.verify("Routing param group created and selected in list", True, True)
            except Exception as e:
                self.verify("Routing param group NOT created !!", True, e.__class__.__name__)

            profiles.click_on_routing_param_group()
            routing_param_groups.set_name_filter(self.name_at_routing_param_groups)
            time.sleep(2)
            actual_result = [routing_param_groups.get_name(), routing_param_groups.get_positive_routes(),
                             routing_param_groups.get_negative_routes(), routing_param_groups.get_parameter(),
                             routing_param_groups.get_value()]
            expected_result = [self.name_at_routing_param_groups, self.positive_routes[0] + ", " + self.positive_routes[1],
                               self.negative_routes[0] + ", " + self.negative_routes[1], self.parameter, self.value]

            try:
                self.verify("Data saved correctly", expected_result, actual_result)
            except Exception as e:
                self.verify("Data saved incorrect!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
