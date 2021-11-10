import time

import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import \
    OrderManagementRulesDefaultResultSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5819(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

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
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
            default_result_sub_wizard.click_on_plus()
            default_result_sub_wizard.set_exec_policy("DMA")
            default_result_sub_wizard.set_percentage("10")
            default_result_sub_wizard.set_venue("BATS")
            time.sleep(1)
            default_result_sub_wizard.click_on_checkmark()
            time.sleep(1)
            default_result_sub_wizard.click_on_plus()
            default_result_sub_wizard.set_exec_policy("DMA")
            default_result_sub_wizard.set_percentage("10")
            default_result_sub_wizard.set_venue("BATS")
            self.verify("DMA created correctly", True, True)
            time.sleep(1)
            default_result_sub_wizard.click_on_checkmark()
            time.sleep(1)
            self.verify("Such record already exists", True, wizard.such_record_already_exists())
            time.sleep(2)
            default_result_sub_wizard.set_venue("BINANCE")
            time.sleep(2)
            default_result_sub_wizard.click_on_checkmark()
            self.verify("DMA second created correctly", True, True)
            time.sleep(2)
            default_result_sub_wizard.click_on_plus()
            default_result_sub_wizard.set_exec_policy("ExternalCare")
            default_result_sub_wizard.set_percentage("10")
            default_result_sub_wizard.set_route("Direct")
            default_result_sub_wizard.click_on_checkmark()
            time.sleep(1)
            self.verify("New external care created correctly", True, True)
            time.sleep(1)
            default_result_sub_wizard.click_on_plus()
            default_result_sub_wizard.set_exec_policy("ExternalCare")
            default_result_sub_wizard.set_percentage("10")
            default_result_sub_wizard.set_route("Direct")
            default_result_sub_wizard.click_on_checkmark()
            time.sleep(1)
            self.verify("Such record already exists", True, wizard.such_record_already_exists())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
