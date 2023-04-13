import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard \
    import InstitutionsValuesSubWizard

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3702(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.institution_name = "QAP-T3702"
        self.new_institution_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lei = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_lei = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_institutions_page()
        time.sleep(2)
        main_page = InstitutionsPage(self.web_driver_container)
        main_page.set_institution_name(self.institution_name)
        time.sleep(1)
        if not main_page.is_searched_institution_found(self.institution_name):
            main_page.click_on_new()
            time.sleep(2)
            value_tab = InstitutionsValuesSubWizard(self.web_driver_container)
            value_tab.set_institution_name(self.institution_name)
            value_tab.set_lei(self.lei)
            wizard = InstitutionsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_institution_name(self.institution_name)
            time.sleep(1)

    def test_context(self):
        try:
            self.precondition()

            main_page = InstitutionsPage(self.web_driver_container)
            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)
            value_tab = InstitutionsValuesSubWizard(self.web_driver_container)
            value_tab.set_lei(self.new_lei)
            wizard = InstitutionsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_lei(self.new_lei)
            time.sleep(1)
            self.verify("New LEI value is displayed at main page after change", True,
                        main_page.is_searched_institution_found(self.new_lei))

            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_clone()
            time.sleep(2)
            value_tab.set_institution_name(self.new_institution_name)
            value_tab.set_lei(self.lei)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_institution_name(self.new_institution_name)
            time.sleep(1)
            self.verify("Cloned Instrument is created and displayed", True,
                        main_page.is_searched_institution_found(self.new_institution_name))

            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)
            wizard.click_on_values_tab()
            time.sleep(1)
            self.verify("Values tab is collapsed", False, value_tab.is_tab_collapsed())

            common_page = CommonPage(self.web_driver_container)
            common_page.click_on_info_error_message_pop_up()
            wizard.click_on_close()
            if wizard.is_leave_page_confirmation_pop_up_displayed():
                wizard.click_on_ok_button()
            time.sleep(2)
            main_page.click_on_download_csv()
            time.sleep(2)
            actual_result = False
            for i in main_page.get_csv_context():
                if self.institution_name in i.values():
                    actual_result = True

            self.verify("Download CSV button is worked", True, actual_result)
            main_page.clear_download_directory()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
