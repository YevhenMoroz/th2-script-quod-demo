import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.main_page import \
    OrderVelocityLimitsPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.values_sub_wizard import \
    OrderVelocityLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.wizard import \
    OrderVelocityLimitsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3592(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.order_velocity_limit_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = '12'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_order_velocity_page()
        time.sleep(2)
        page = OrderVelocityLimitsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = OrderVelocityLimitsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_order_velocity_limit_name(self.order_velocity_limit_name)
        time.sleep(1)
        values_sub_wizard.set_moving_time_window(self.moving_time_window)
        time.sleep(1)
        wizard = OrderVelocityLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.order_velocity_limit_name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = OrderVelocityLimitsPage(self.web_driver_container)
            page.click_on_delete(True)
            time.sleep(2)
            try:
                page.set_name(self.order_velocity_limit_name)
                time.sleep(2)
                page.click_on_more_actions()
                self.verify("Entity not deleted", True, False)
            except Exception:
                self.verify("Entity deleted correctly", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
