import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_schedules_sub_wizard import \
    ClientTiersSchedulesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9437(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = self.schedule = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.core_spot_price_strategy = self.data_set.get_core_spot_price_strategy("core_spot_price_strategy_3")
        self.tod_end_time = '23:33:33'
        self.day = 'Monday'
        self.from_time = '01:00:00'
        self.to_time = '02:00:00'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = ClientTiersPage(self.web_driver_container)
            main_page.click_on_new()
            values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
            values_tab.click_on_manage_button_for_schedules()
            schedule_wizard = ClientTiersSchedulesSubWizard(self.web_driver_container)
            schedule_wizard.click_on_plus_button_at_schedule_name()
            schedule_wizard.set_schedule_name(self.schedule)
            schedule_wizard.click_on_plus_button_at_schedules()
            schedule_wizard.set_day(self.day)
            schedule_wizard.set_from_time(self.from_time)
            schedule_wizard.set_to_time(self.to_time)
            schedule_wizard.click_on_checkmark_button_at_schedules()
            schedule_wizard.click_on_checkmark_button_at_schedule_name()

            wizard = ClientTiersWizard(self.web_driver_container)
            wizard.click_on_go_back_button()

            values_tab.set_name(self.name)
            values_tab.set_core_spot_price_strategy(self.core_spot_price_strategy)
            values_tab.set_tod_end_time(self.tod_end_time)
            values_tab.select_schedule_checkbox()
            values_tab.set_schedule(self.schedule)
            wizard.click_on_save_changes()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_result = [self.name, self.schedule]
            actual_result = [values_tab.get_name(), values_tab.get_schedule()]

            self.verify("New Client Tiers with new Schedule created", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
