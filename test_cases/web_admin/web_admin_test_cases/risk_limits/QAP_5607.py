import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_dimensions_sub_wizard import \
    OrderVelocityLimitDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_page import \
    OrderVelocityLimitPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_values_sub_wizard import \
    OrderVelocityLimitValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_wizard import \
    OrderVelocityLimitWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5607(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.order_velocity_limit_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = '25'
        self.max_order_actions = '3'
        self.client = 'CLIENT1'
        self.side = 'Buy'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_order_velocity_page()
        time.sleep(2)
        page = OrderVelocityLimitPage(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard = OrderVelocityLimitValuesSubWizard(self.web_driver_container)
        wizard = OrderVelocityLimitWizard(self.web_driver_container)
        values_sub_wizard.set_order_velocity_limit_name(self.order_velocity_limit_name)
        time.sleep(1)
        values_sub_wizard.set_moving_time_window(self.moving_time_window)
        time.sleep(1)
        values_sub_wizard.set_max_order_actions(self.max_order_actions)
        time.sleep(1)
        dimensions_sub_wizard = OrderVelocityLimitDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.set_client(self.client)
        time.sleep(1)
        dimensions_sub_wizard.set_side(self.side)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.order_velocity_limit_name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            values_sub_wizard = OrderVelocityLimitValuesSubWizard(self.web_driver_container)
            dimensions_sub_wizard = OrderVelocityLimitDimensionsSubWizard(self.web_driver_container)
            expected_content = [self.order_velocity_limit_name,
                                self.moving_time_window,
                                self.max_order_actions,
                                self.client,
                                self.side]

            actual_content = [values_sub_wizard.get_order_velocity_limit_name(),
                              values_sub_wizard.get_moving_time_window(),
                              values_sub_wizard.get_max_order_actions(),
                              dimensions_sub_wizard.get_client(),
                              dimensions_sub_wizard.get_side()]

            self.verify("Is order velocity changed correctly", expected_content, actual_content)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
