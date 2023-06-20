import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_schedules_sub_wizard import \
    ClientTiersSchedulesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3880(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.days = ["Monday", "Friday", "Tuesday"]
        self.from_time = "15:00:00"
        self.to_time = "18:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()

        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.click_on_new()
        client_tiers_values_sub_wizard = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_sub_wizard.click_on_manage_button_for_schedules()

        schedules_wizard = ClientTiersSchedulesSubWizard(self.web_driver_container)
        schedules_wizard.click_on_plus_button_at_schedule_name()
        schedules_wizard.set_schedule_name(self.name)
        schedules_wizard.click_on_plus_button_at_schedules()
        schedules_wizard.set_day(self.days[0])
        schedules_wizard.set_from_time(self.from_time)
        schedules_wizard.set_to_time(self.to_time)
        schedules_wizard.click_on_checkmark_button_at_schedules()
        schedules_wizard.click_on_plus_button_at_schedules()
        schedules_wizard.set_day(self.days[1])
        schedules_wizard.set_from_time(self.from_time)
        schedules_wizard.set_to_time(self.to_time)
        schedules_wizard.click_on_checkmark_button_at_schedules()
        schedules_wizard.click_on_plus_button_at_schedules()
        schedules_wizard.set_day(self.days[2])
        schedules_wizard.set_from_time(self.from_time)
        schedules_wizard.set_to_time(self.to_time)
        schedules_wizard.click_on_checkmark_button_at_schedules()
        schedules_wizard.click_on_checkmark_button_at_schedule_name()
        schedules_wizard.set_schedule_name_filter(self.name)
        time.sleep(1)

        self.verify("Schedules has been create", True,
                    schedules_wizard.is_schedule_name_entity_found_by_name(self.name))

        schedules_wizard.click_on_delete_button_at_schedule_name()

