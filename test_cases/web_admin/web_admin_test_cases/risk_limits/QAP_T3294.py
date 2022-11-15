import random
import string
import sys
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


class QAP_T3294(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.order_velocity_limit_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = '25'
        self.max_quantity = '1'
        self.max_amount = '2'
        self.max_order_actions = '3'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_velocity_page()

    def test_context(self):
        try:
            self.precondition()

            page = OrderVelocityLimitsPage(self.web_driver_container)
            page.click_on_new()

            wizard = OrderVelocityLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            values_tab = OrderVelocityLimitsValuesSubWizard(self.web_driver_container)
            values_tab.set_order_velocity_limit_name(self.order_velocity_limit_name)
            values_tab.set_moving_time_window(self.moving_time_window)
            values_tab.set_max_quantity(self.max_quantity)
            values_tab.set_max_amount(self.max_amount)
            values_tab.set_max_order_actions(self.max_order_actions)

            self.verify("Values tab filled", [self.order_velocity_limit_name, self.moving_time_window,
                                              self.max_quantity, self.max_amount, self.max_order_actions],
                        [values_tab.get_order_velocity_limit_name(), values_tab.get_moving_time_window(),
                         values_tab.get_max_quantity(), values_tab.get_max_amount(), values_tab.get_max_order_actions()])

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
