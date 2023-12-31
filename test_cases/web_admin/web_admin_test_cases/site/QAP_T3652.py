import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard import \
    InstitutionsValuesSubWizard
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3652(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = self.data_set.get_institution("institution_2")
        self.lei = "test"
        self.ctm_bic = "test"
        self.counterpart = self.data_set.get_counterpart("counterpart_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_institutions_page()
        page = InstitutionsPage(self.web_driver_container)
        page.set_institution_name(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_edit()
        values_sub_wizard = InstitutionsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_lei(self.lei)
        values_sub_wizard.set_ctm_bic(self.ctm_bic)
        values_sub_wizard.set_counterpart(self.counterpart)
        wizard = InstitutionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        page.set_institution_name(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_edit()

    def test_context(self):
        self.precondition()
        values_sub_wizard = InstitutionsValuesSubWizard(self.web_driver_container)
        expected_values = [self.lei,
                           self.ctm_bic,
                           self.counterpart]
        actual_values = [values_sub_wizard.get_lei(),
                         values_sub_wizard.get_ctm_bic(),
                         values_sub_wizard.get_counterpart()]
        self.verify("Is Institution edited correctly", expected_values, actual_values)
