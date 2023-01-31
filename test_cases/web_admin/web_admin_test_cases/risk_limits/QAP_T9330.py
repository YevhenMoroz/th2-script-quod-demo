import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards \
    import ValuesTab, DimensionsTab, MainWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9330(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.order_type = 'Limit'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def postconditions(self):
        main_page = MainPage(self.web_driver_container)
        for i in self.name:
            main_page.set_name_filter(i)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_delete(True)
            time.sleep(1)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_risk_limit_dimension_page()
            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[0])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_order_type(self.order_type)

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name[0])
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_result = [self.name[0], self.order_type]
            actual_result = [values_tab.get_name(), dimensions_tab.get_order_type()]
            self.verify("New rule is created with all entered fields.", expected_result, actual_result)
            wizard.click_on_save_changes()

            common_act = CommonPage(self.web_driver_container)
            common_act.click_on_info_error_message_pop_up()

            main_page.click_on_new_button()
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[1])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_order_type(self.order_type)
            dimensions_tab.select_display_order_checkbox()

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name[1])
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_result = [self.name[1], self.order_type, True]
            actual_result = [values_tab.get_name(), dimensions_tab.get_order_type(),
                             dimensions_tab.is_display_order_checkbox_selected()]
            self.verify("New rule is created with all entered fields.", expected_result, actual_result)
            wizard.click_on_save_changes()

            self.postconditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
