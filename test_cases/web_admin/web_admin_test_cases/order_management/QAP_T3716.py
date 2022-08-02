import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import \
    OrderManagementRulesDefaultResultSubWizard
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3716(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.exec_policy = self.data_set.get_exec_policy("exec_policy_3")
        self.percentage = "100"
        self.route = self.data_set.get_route("route_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_when_order_management_tab_is_open()
        time.sleep(2)
        page = OrderManagementRulesPage(self.web_driver_container)
        page.click_on_new_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
            try:
                default_result_sub_wizard.click_on_edit()
                time.sleep(1)
                default_result_sub_wizard.click_on_plus_at_results()
                time.sleep(1)
                default_result_sub_wizard.set_exec_policy(self.exec_policy)
                default_result_sub_wizard.set_percentage(self.percentage)
                default_result_sub_wizard.set_route(self.route)
                default_result_sub_wizard.click_on_checkmark()
                time.sleep(1)
                default_result_sub_wizard.click_on_edit()
                self.verify("Is route field contains correctly value", self.route,
                            default_result_sub_wizard.get_route())
            except Exception as e:
                self.verify("Route field is NOT contains correctly value", self.route, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
