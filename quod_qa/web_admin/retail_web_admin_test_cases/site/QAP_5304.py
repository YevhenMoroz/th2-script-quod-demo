import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.institution.institution_values_sub_wizard import \
    InstitutionsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5304(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = "LOAD"
        self.lei = "test"
        self.ctm_bic = "test"
        self.counterpart = "TCOther"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_institutions_page()
        page = InstitutionsPage(self.web_driver_container)
        page.set_institution_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard = InstitutionsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_lei(self.lei)
        time.sleep(1)
        values_sub_wizard.set_ctm_bic(self.ctm_bic)
        time.sleep(1)
        values_sub_wizard.set_counterpart(self.counterpart)
        time.sleep(1)
        wizard = InstitutionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        page.set_institution_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

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
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
