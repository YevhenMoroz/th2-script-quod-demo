import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_dimensions_sub_wizard import \
    ExternalCheckDimensionsSubWizard
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_page import ExternalCheckPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_values_sub_wizard import \
    ExternalCheckValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_wizard import ExternalCheckWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4851(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'AMEX'
        self.client = 'CLIENT1'
        self.instr_type = 'Bond'
        self.client_group = 'Group1'

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
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
