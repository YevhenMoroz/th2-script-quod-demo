import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3406(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.test_data = {"zones_user": {"login": "adm_zone", "password": "adm_zone"},
                          "locations_user": {"login": "adm_loca", "password": "adm_loca"},
                          "desks_user": {"login": "adm_desk", "password": "adm_desk"}}

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = 'QUOD FINANCIAL'
        self.account = ''

    def test_context(self):
        try:
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.test_data["zones_user"]["login"],
                                          self.test_data["zones_user"]["password"])
            time.sleep(2)
            side_menu = SideMenu(self.web_driver_container)
            self.verify("WashBook page is not displayed for zones user", False,
                        side_menu.is_washbook_page_tab_displayed())
            self.verify("WashBookRule page is not displayed for zones user", False,
                        side_menu.is_washbook_rule_page_tab_displayed())
            common_act = CommonPage(self.web_driver_container)
            common_act.click_on_user_icon()
            common_act.click_on_logout()
            common_act.refresh_page(True)
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.test_data["locations_user"]["login"],
                                          self.test_data["locations_user"]["password"])
            time.sleep(2)
            self.verify("WashBook page is not displayed for locations user", False,
                        side_menu.is_washbook_page_tab_displayed())
            self.verify("WashBookRule page is not displayed for locations user", False,
                        side_menu.is_washbook_rule_page_tab_displayed())
            common_act.click_on_user_icon()
            common_act.click_on_logout()
            common_act.refresh_page(True)
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.test_data["desks_user"]["login"],
                                          self.test_data["desks_user"]["password"])
            time.sleep(2)
            self.verify("WashBook page is not displayed for desks user", False,
                        side_menu.is_washbook_rule_page_tab_displayed())
            self.verify("WashBookRule page is not displayed for desks user", False,
                        side_menu.is_washbook_rule_page_tab_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
