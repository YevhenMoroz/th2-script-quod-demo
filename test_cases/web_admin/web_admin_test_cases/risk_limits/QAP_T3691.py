import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.external_checks.dimensions_sub_wizard import \
    ExternalCheckDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.external_checks.main_page import ExternalCheckPage
from test_framework.web_admin_core.pages.risk_limits.external_checks.values_sub_wizard import \
    ExternalCheckValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.external_checks.wizard import ExternalCheckWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3691(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.client = self.data_set.get_client("client_1")
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.client_group = self.data_set.get_client_group("client_group_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_external_check_page()
        time.sleep(2)
        page = ExternalCheckPage(self.web_driver_container)
        wizard = ExternalCheckWizard(self.web_driver_container)
        values_sub_wizard = ExternalCheckValuesSubWizard(self.web_driver_container)
        dimensions_sub_wizard = ExternalCheckDimensionsSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        dimensions_sub_wizard.set_venue(self.venue)
        dimensions_sub_wizard.set_client(self.client)
        dimensions_sub_wizard.set_instr_type(self.instr_type)
        dimensions_sub_wizard.set_client_group(self.client_group)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = ExternalCheckPage(self.web_driver_container)
            expected_values = [self.name,
                               self.venue,
                               self.client,
                               self.instr_type,
                               self.client_group]
            actual_values = [page.get_name(),
                             page.get_venue(),
                             page.get_client(),
                             page.get_instr_type(),
                             page.get_client_group()]
            self.verify("Is entity saved correctly?",
                        expected_values, actual_values)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
