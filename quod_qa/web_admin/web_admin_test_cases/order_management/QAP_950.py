import random
import string

import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage

from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_values_sub_wizard import \
    OrderManagementRulesValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_950(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMERICAN STOCK EXCHANGE"
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)
        page.click_on_new_button()

    def test_context(self):

        try:
            self.precondition()

            values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            self.verify("Incorrect or missing values displayed - without any information", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            values_sub_wizard.set_name(self.name)
            wizard.click_on_save_changes()
            self.verify("Incorrect or missing values displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
