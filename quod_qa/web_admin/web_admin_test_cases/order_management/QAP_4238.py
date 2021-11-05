import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_conditions_sub_wizard import \
    OrderManagementRulesConditionsSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import \
    OrderManagementRulesDefaultResultSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_values_sub_wizard import \
    OrderManagementRulesValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4238(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "COINBASE"
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)
        values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
        conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
        default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
        wizard = OrderManagementRulesWizard(self.web_driver_container)

        page.click_on_new_button()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        time.sleep(2)
        values_sub_wizard.set_venue(self.venue)
        time.sleep(1)
        conditions_sub_wizard.click_on_plus()
        time.sleep(1)
        conditions_sub_wizard.set_name(self.condition_name)
        time.sleep(1)
        conditions_sub_wizard.set_qty_precision("100")
        conditions_sub_wizard.click_on_add_condition()
        time.sleep(2)
        conditions_sub_wizard.set_right_side_at_conditional_logic("CLIENT1")
        conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
        conditions_sub_wizard.set_exec_policy("DMA")
        time.sleep(1)
        conditions_sub_wizard.set_percentage("100")
        conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
        time.sleep(1)
        conditions_sub_wizard.click_on_checkmark()
        default_result_sub_wizard.set_default_result_name("test")
        default_result_sub_wizard.click_on_plus()
        time.sleep(1)
        default_result_sub_wizard.set_exec_policy("Care")
        default_result_sub_wizard.set_percentage("100")
        default_result_sub_wizard.click_on_checkmark()
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = OrderManagementRulesPage(self.web_driver_container)
            conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
            values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            page = OrderManagementRulesPage(self.web_driver_container)
            default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
            try:
                page.click_on_enabled_disable(True)
                time.sleep(3)
                page.click_on_new_button()
                time.sleep(2)
                values_sub_wizard.set_name(self.name)
                time.sleep(2)
                values_sub_wizard.set_venue(self.venue)
                time.sleep(1)
                conditions_sub_wizard.click_on_plus()
                time.sleep(1)
                conditions_sub_wizard.set_name(self.condition_name)
                time.sleep(1)
                conditions_sub_wizard.set_qty_precision("100")
                conditions_sub_wizard.click_on_add_condition()
                time.sleep(2)
                conditions_sub_wizard.set_right_side_at_conditional_logic("CLIENT1")
                conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
                conditions_sub_wizard.set_exec_policy("DMA")
                time.sleep(1)
                conditions_sub_wizard.set_percentage("100")
                conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
                time.sleep(1)
                conditions_sub_wizard.click_on_checkmark()
                default_result_sub_wizard.set_default_result_name("test")
                default_result_sub_wizard.click_on_plus()
                time.sleep(1)
                default_result_sub_wizard.set_exec_policy("Care")
                default_result_sub_wizard.set_percentage("100")
                default_result_sub_wizard.click_on_checkmark()
                time.sleep(1)
                wizard.click_on_save_changes()
                time.sleep(2)
                page.set_name_filter(self.name)
                time.sleep(2)
                page.click_on_enabled_field()
                page.set_enabled_filter("true")
                time.sleep(2)
                page.click_on_more_actions()
                self.verify("Same entity created (normal)!", True, True)

            except Exception:
                self.verify("Entity NOT created ", True, False)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
