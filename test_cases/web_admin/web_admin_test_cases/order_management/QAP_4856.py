import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_conditions_sub_wizard import \
    OrderManagementRulesConditionsSubWizard
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4856(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_execution_strategies_when_order_management_tab_is_open()
        side_menu.wait_for_button_to_become_active()
        page = OrderManagementRulesPage(self.web_driver_container)
        conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)

        page.click_on_new_button()
        time.sleep(2)
        conditions_sub_wizard.click_on_plus()
        time.sleep(1)
        conditions_sub_wizard.set_name("test 1")
        time.sleep(1)
        conditions_sub_wizard.set_qty_precision("100")
        conditions_sub_wizard.click_on_add_condition()
        time.sleep(2)
        conditions_sub_wizard.set_right_side_at_conditional_logic(self.data_set.get_client("client_1"))
        conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
        conditions_sub_wizard.set_exec_policy(self.data_set.get_exec_policy("exec_policy_2"))
        time.sleep(1)
        conditions_sub_wizard.set_percentage("100")
        conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
        conditions_sub_wizard.click_on_checkmark()
        time.sleep(1)
        conditions_sub_wizard.click_on_plus()
        time.sleep(1)
        conditions_sub_wizard.set_name("test 2")
        time.sleep(1)
        conditions_sub_wizard.set_qty_precision("100")
        conditions_sub_wizard.click_on_add_condition()
        time.sleep(2)
        conditions_sub_wizard.set_right_side_at_conditional_logic(self.data_set.get_client("client_1"))
        conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
        conditions_sub_wizard.set_exec_policy(self.data_set.get_exec_policy("exec_policy_2"))
        time.sleep(1)
        conditions_sub_wizard.set_percentage("100")
        conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
        time.sleep(1)
        conditions_sub_wizard.set_name_filter("test 2")
        time.sleep(2)
        conditions_sub_wizard.click_on_delete_at_results_sub_wizard()
        time.sleep(2)
        conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
        conditions_sub_wizard.set_exec_policy(self.data_set.get_exec_policy("exec_policy_1"))
        time.sleep(1)
        conditions_sub_wizard.set_percentage("100")
        conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
        time.sleep(1)
        conditions_sub_wizard.click_on_checkmark()
        time.sleep(1)
        conditions_sub_wizard.set_name_filter("test 1")
        time.sleep(2)
        conditions_sub_wizard.click_on_edit()
        time.sleep(1)
        conditions_sub_wizard.click_on_edit_at_results_sub_wizard()
        time.sleep(1)

    def test_context(self):

        try:
            self.precondition()
            conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
            self.verify("After edited, Conditions have another values", "DMA", conditions_sub_wizard.get_exec_policy())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
