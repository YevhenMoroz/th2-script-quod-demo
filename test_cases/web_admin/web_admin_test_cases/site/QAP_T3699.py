import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard import \
    InstitutionsValuesSubWizard
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3699(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_institutions_page()
        time.sleep(2)
        page = InstitutionsPage(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(1)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard = InstitutionsValuesSubWizard(self.web_driver_container)
        name = values_sub_wizard.get_institution_name()
        wizard = InstitutionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_institution_name(name)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            wizard = InstitutionsWizard(self.web_driver_container)
            self.verify("such record already exist message displayed", True,
                        wizard.is_such_record_exists_massage_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
