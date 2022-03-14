import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage

from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_values_sub_wizard import \
    OrderManagementRulesValuesSubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4158(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.venue = self.data_set.get_venue_by_name("venue_8")
        self.instr_type = self.data_set.get_instr_type("instr_type_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)
        time.sleep(2)
        page.click_on_change_criteria()
        time.sleep(1)
        page.set_first_criteria("Venue")
        time.sleep(1)
        page.set_second_criteria("ListingGroup")
        time.sleep(1)
        page.set_third_criteria("InstrumentType")
        time.sleep(1)
        page.click_on_change_criteria_for_saving(True)
        time.sleep(1)
        side_menu.open_order_management_rules_page()
        time.sleep(2)
        page.click_on_new_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            try:
                values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
                values_sub_wizard.set_venue(self.venue)
                values_sub_wizard.set_listing_group("test")
                values_sub_wizard.set_instr_type(self.instr_type)
                self.verify("Criteria changed correctly and displayed at wizard", True, True)
            except Exception as e:
                self.verify("Criteria don't changed !!! Error!!!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
