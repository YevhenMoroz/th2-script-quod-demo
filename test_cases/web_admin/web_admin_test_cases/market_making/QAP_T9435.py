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
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9435(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.schedule = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_schedule_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
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
            schedule_wizard.set_schedule_name_filter(self.schedule)
            time.sleep(1)
            schedule_wizard.click_on_edit_button_at_schedule_name()
            schedule_wizard.set_schedule_name(self.new_schedule_name)
            schedule_wizard.click_on_checkmark_button_at_schedule_name()

            schedule_wizard.set_schedule_name_filter(self.schedule)
            time.sleep(1)
            self.verify("Old name not displayed", False,
                        schedule_wizard.is_schedule_name_entity_found_by_name(self.schedule))
            schedule_wizard.set_schedule_name_filter(self.new_schedule_name)
            time.sleep(1)
            self.verify("New name displayed", True,
                        schedule_wizard.is_schedule_name_entity_found_by_name(self.new_schedule_name))

            common_act = CommonPage(self.web_driver_container)
            common_act.refresh_page(True)
            time.sleep(1)
            schedule_wizard.set_schedule_name_filter(self.new_schedule_name)
            time.sleep(1)
            self.verify("New name displayed", True,
                        schedule_wizard.is_schedule_name_entity_found_by_name(self.new_schedule_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
