import sys
import time
import traceback
import string
import random

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_page \
    import ClientGroupsPage
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_wizard import ClientGroupsWizard
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_values_sub_wizard \
    import ClientGroupsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_dimensions_sub_wizard \
    import ClientGroupsDimensionsSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4022(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.block_approval = ''
        self.confirmation_service = ''
        self.user_manager = ''
        self.price_precision = random.randint(1, 100)
        self.default_execution_strategy_type = ''
        self.default_execution_strategy = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        main_page = ClientGroupsPage(self.web_driver_container)
        wizard = ClientGroupsWizard(self.web_driver_container)
        values_tab = ClientGroupsValuesSubWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_client_groups_page()
        main_page.click_on_new()
        values_tab.set_name(self.name)
        wizard.click_on_save_changes()

    def post_condition(self):
        main_page = ClientGroupsPage(self.web_driver_container)

        main_page.set_name(self.new_name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):
        main_page = ClientGroupsPage(self.web_driver_container)
        wizard = ClientGroupsWizard(self.web_driver_container)
        values_tab = ClientGroupsValuesSubWizard(self.web_driver_container)
        policies_tab = ClientGroupsDimensionsSubWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            values_tab.set_name(self.new_name)
            self.block_approval = random.choice(values_tab.get_all_block_approval_from_drop_menu())
            values_tab.set_block_approval(self.block_approval)
            self.confirmation_service = random.choice(values_tab.get_all_confirmation_service_from_drop_menu())
            values_tab.set_confirmation_service(self.confirmation_service)
            self.user_manager = random.choice(values_tab.get_all_user_manager_from_drop_menu())
            values_tab.set_user_manager(self.user_manager)
            values_tab.set_price_precision(self.price_precision)

            self.default_execution_strategy_type = random.choice(
                policies_tab.get_all_default_execution_strategy_type_from_drop_menu())
            policies_tab.set_default_execution_strategy_type(self.default_execution_strategy_type)
            self.default_execution_strategy = random.choice(
                policies_tab.get_all_default_execution_strategy_from_drop_menu())
            policies_tab.set_default_execution_strategy(self.default_execution_strategy)
            wizard.click_on_save_changes()

            main_page.set_name(self.new_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            actual_result = [values_tab.get_name(), values_tab.get_block_approval(),
                             values_tab.get_confirmation_service(), values_tab.get_user_manager(),
                             values_tab.get_price_precision(), policies_tab.get_default_execution_strategy_type(),
                             policies_tab.get_default_execution_strategy()]
            expected_result = [self.new_name, self.block_approval, self.confirmation_service, self.user_manager,
                               self.price_precision, self.default_execution_strategy_type,
                               self.default_execution_strategy]

            self.verify("Changed data save correct", expected_result, actual_result)

            wizard.click_on_save_changes()

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
