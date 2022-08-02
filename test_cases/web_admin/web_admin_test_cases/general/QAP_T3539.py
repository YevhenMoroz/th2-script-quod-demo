import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.mdentitlements.mdentitlements_dimensions_sub_wizard import \
    MDEntitlementsDimensionsSubWizard
from test_framework.web_admin_core.pages.general.mdentitlements.mdentitlements_page import MDEntitlementsPage
from test_framework.web_admin_core.pages.general.mdentitlements.mdentitlements_wizard import MDEntitlementsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3539(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.user = self.data_set.get_user("user_2")
        self.desk = self.data_set.get_desk("desk_1")
        self.location = self.data_set.get_location("location_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_mdentitlements_page()
        page = MDEntitlementsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        dimensions_sub_wizard = MDEntitlementsDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.set_user(self.user)
        dimensions_sub_wizard.set_desk(self.desk)
        dimensions_sub_wizard.set_location(self.location)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            wizard = MDEntitlementsWizard(self.web_driver_container)
            page = MDEntitlementsPage(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            dimensions_sub_wizard = MDEntitlementsDimensionsSubWizard(self.web_driver_container)
            self.verify("Both Desk and Location can not be filled message displayed", True,
                        wizard.is_both_desk_and_location_can_be_filled_message_displayed())
            dimensions_sub_wizard.clear_location_field()
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_user(self.user)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            expected_pdf_result = [self.user,
                                   self.desk]
            self.verify("Is pdf contains correctly values", True,
                        page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_result))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
