import sys
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


class QAP_T3652(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.name = "LOAD"
        self.lei = "test"
        self.ctm_bic = "test"
        self.counterpart = "TCOther"

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
        try:
            self.precondition()
            values_sub_wizard = InstitutionsValuesSubWizard(self.web_driver_container)
            expected_values = [self.lei,
                               self.ctm_bic,
                               self.counterpart]
            actual_values = [values_sub_wizard.get_lei(),
                             values_sub_wizard.get_ctm_bic(),
                             values_sub_wizard.get_counterpart()]
            self.verify("Is Institution edited correctly", expected_values, actual_values)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
