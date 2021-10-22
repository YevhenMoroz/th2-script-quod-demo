import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_page import \
    OrderVelocityLimitPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_values_sub_wizard import \
    OrderVelocityLimitValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_wizard import \
    OrderVelocityLimitWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5606(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm03"
        self.password = "adm03"
        self.order_velocity_limit_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = '12'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_order_velocity_page()
        time.sleep(2)
        page = OrderVelocityLimitPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = OrderVelocityLimitValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_order_velocity_limit_name(self.order_velocity_limit_name)
        time.sleep(1)
        values_sub_wizard.set_moving_time_window(self.moving_time_window)
        time.sleep(1)
        wizard = OrderVelocityLimitWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.order_velocity_limit_name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = OrderVelocityLimitPage(self.web_driver_container)
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
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
