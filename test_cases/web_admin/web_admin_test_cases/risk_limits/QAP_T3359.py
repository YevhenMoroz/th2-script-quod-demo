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


class QAP_T3359(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.qty_amt_values = [str(random.randint(1, 10000)) for _ in range(8)]
        self.currency = 'EUR'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_positions_limits_page()
        position_page = PositionLimitsPage(self.web_driver_container)
        position_page.click_on_new()
        values_tab = PositionLimitsValuesSubWizard(self.web_driver_container)
        values_tab.set_description(self.description)
        values_tab.set_min_soft_qty(self.qty_amt_values[0])
        values_tab.set_min_soft_amt(self.qty_amt_values[1])
        values_tab.set_max_soft_qty(self.qty_amt_values[2])
        values_tab.set_max_soft_amt(self.qty_amt_values[3])
        values_tab.set_min_hard_qty(self.qty_amt_values[4])
        values_tab.set_min_hard_amt(self.qty_amt_values[5])
        values_tab.set_max_hard_qty(self.qty_amt_values[6])
        values_tab.set_max_hard_amt(self.qty_amt_values[7])
        values_tab.set_currency(self.currency)
        wizard = PositionLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            position_page = PositionLimitsPage(self.web_driver_container)
            position_page.set_description(self.description)
            position_page.set_min_soft_qty(self.qty_amt_values[0])
            position_page.set_min_soft_amt(self.qty_amt_values[1])
            position_page.set_max_soft_qty(self.qty_amt_values[2])
            position_page.set_max_soft_amt(self.qty_amt_values[3])
            position_page.set_min_qty(self.qty_amt_values[4])
            position_page.set_min_amt(self.qty_amt_values[5])
            position_page.set_max_qty(self.qty_amt_values[6])
            position_page.set_max_amt(self.qty_amt_values[7])
            position_page.set_currency(self.currency)
            time.sleep(1)
            self.verify('Entity displayed', True, position_page.is_searched_entity_found(self.currency))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
