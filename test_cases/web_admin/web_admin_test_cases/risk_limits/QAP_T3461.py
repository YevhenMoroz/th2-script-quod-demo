import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_page import PositionLimitsPage
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_values_sub_wizard \
    import PositionLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_wizard import PositionLimitsWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3461(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = 'QAP6384'
        self.new_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.qty_amt_values = [str(random.randint(1, 10000)) for _ in range(8)]
        self.currency = ['EUR', 'USD']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_positions_limits_page()
        time.sleep(2)
        position_page = PositionLimitsPage(self.web_driver_container)
        position_page.set_description(self.description)
        time.sleep(2)
        if not position_page.is_searched_entity_found(self.description):
            position_page.click_on_new()
            time.sleep(2)
            values_tab = PositionLimitsValuesSubWizard(self.web_driver_container)
            values_tab.set_description(self.description)
            wizard = PositionLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            position_page.set_description(self.description)
            time.sleep(1)

    def post_conditions(self):
        position_page = PositionLimitsPage(self.web_driver_container)
        position_page.click_on_more_actions()
        time.sleep(1)
        position_page.click_on_edit()
        time.sleep(2)
        values_tab = PositionLimitsValuesSubWizard(self.web_driver_container)
        values_tab.set_description(self.description)
        values_tab.set_currency(self.currency[1])
        wizard = PositionLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            position_page = PositionLimitsPage(self.web_driver_container)
            position_page.click_on_more_actions()
            time.sleep(1)
            position_page.click_on_edit()
            time.sleep(2)
            values_tab = PositionLimitsValuesSubWizard(self.web_driver_container)
            values_tab.set_description(self.new_description)
            values_tab.set_min_soft_qty(self.qty_amt_values[0])
            values_tab.set_min_soft_amt(self.qty_amt_values[1])
            values_tab.set_max_soft_qty(self.qty_amt_values[2])
            values_tab.set_max_soft_amt(self.qty_amt_values[3])
            values_tab.set_min_hard_qty(self.qty_amt_values[4])
            values_tab.set_min_hard_amt(self.qty_amt_values[5])
            values_tab.set_max_hard_qty(self.qty_amt_values[6])
            values_tab.set_max_hard_amt(self.qty_amt_values[7])
            values_tab.set_currency(self.currency[0])
            wizard = PositionLimitsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            position_page.set_description(self.new_description)
            time.sleep(1)

            self.verify("New data saved correctly", [self.new_description, self.qty_amt_values[0],
                                                     self.qty_amt_values[1], self.qty_amt_values[2],
                                                     self.qty_amt_values[3], self.qty_amt_values[4],
                                                     self.qty_amt_values[5], self.qty_amt_values[6],
                                                     self.qty_amt_values[7], self.currency[0]],
                        [position_page.get_description(), position_page.get_min_soft_qty(),
                         position_page.get_min_soft_amt(), position_page.get_max_soft_qty(),
                         position_page.get_max_soft_amt(), position_page.get_min_qty(),
                         position_page.get_min_amt(), position_page.get_max_qty(),
                         position_page.get_max_amt(), position_page.get_currency()])

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
