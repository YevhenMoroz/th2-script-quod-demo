import random
import string
import sys
import time
import traceback
from datetime import date, timedelta

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage

from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.markets.venues.venues_profiles_sub_wizard import VenuesProfilesSubWizard
from test_framework.web_admin_core.pages.markets.venues.nested_wizards.venues_holiday_sub_wizard \
    import VenuesHolidaySubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8293(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.holiday_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.holiday_day = str(date.today() + timedelta(days=1))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()

    def test_context(self):

        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.click_on_new()
            profiles_tab = VenuesProfilesSubWizard(self.web_driver_container)
            profiles_tab.click_on_holiday_manage_button()
            holidays_wizard = VenuesHolidaySubWizard(self.web_driver_container)
            holidays_wizard.click_on_plus_button()
            holidays_wizard.set_holiday_name(self.holiday_name)
            holidays_wizard.click_on_plus_button_at_holiday_calendars()
            holidays_wizard.set_date(self.holiday_day)
            holidays_wizard.click_on_checkmark_at_holiday_calendars()
            holidays_wizard.click_on_checkmark()
            time.sleep(1)

            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_go_back_button()
            time.sleep(1)
            profiles_tab.set_holiday(self.holiday_name)
            self.verify("Newly Holidays select", self.holiday_name, profiles_tab.get_holiday())

            profiles_tab.click_on_holiday_manage_button()
            holidays_wizard.set_holiday_name_filter(self.holiday_name)
            time.sleep(1)
            holidays_wizard.click_on_delete()
            wizard.click_on_ok_button()
            time.sleep(1)
            self.verify('Holiday not displaying after delete', False,
                        holidays_wizard.is_holiday_found(self.holiday_name))

            wizard.click_on_go_back_button()
            time.sleep(0.5)
            try:
                profiles_tab.set_holiday(self.holiday_name)
                self.verify('Delete Trading Phase Profile can be selected in the Venue wizard', True, False)
            except:
                self.verify('Trading Phase Profile not displaying  in the Venue wizard after delete', True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
