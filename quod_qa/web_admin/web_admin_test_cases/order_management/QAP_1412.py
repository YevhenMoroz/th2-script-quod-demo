import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_conditions_sub_wizard import \
    OrderManagementRulesConditionsSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1412(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"

        self.conditional_logic_left_side = " Side "
        self.conditional_logic_right_side = "Buy"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)

        page.click_on_new_button()
        conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
        conditions_sub_wizard.click_on_plus()
        conditions_sub_wizard.click_on_add_condition()
        conditions_sub_wizard.click_on_left_side()
        conditions_sub_wizard.set_left_side_at_conditional_logic(self.conditional_logic_left_side)
        time.sleep(2)
        conditions_sub_wizard.set_right_side_at_conditional_logic(self.conditional_logic_right_side)

    def test_context(self):

        try:
            self.precondition()
            conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
            conditions_sub_wizard.click_on_checkmark()
            time.sleep(2)
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            self.verify("Is incorrect or missing values message displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
