import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import \
    OrderManagementRulesDefaultResultSubWizard

from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3995(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)
        page.click_on_new_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()

            default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            self.verify("Incorrect or missing values displayed - without any information", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            default_result_sub_wizard.set_default_result_name("test")
            wizard.click_on_save_changes()
            self.verify("Incorrect or missing values displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
