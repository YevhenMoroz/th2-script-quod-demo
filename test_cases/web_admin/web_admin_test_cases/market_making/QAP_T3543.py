import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page \
    import ClientTiersPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3543(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()

    def test_context(self):
        try:
            page = ClientTiersPage(self.web_driver_container)

            self.precondition()
            self.verify("Tooltip for enabled Executable displayed", True, page.is_enabled_executable_tool_tip_appears())
            page.switch_executable_status()
            time.sleep(1)
            self.verify("Is Executable enable", False, page.is_executable_enable())
            self.verify("Tooltip for disabled Executable displayed", True, page.is_disabled_executable_tool_tip_appears())

            self.verify("Tooltip for enabled Pricing displayed", True, page.is_enabled_pricing_tool_tip_appears())
            page.switch_pricing_status()
            time.sleep(1)
            self.verify("Is Pricing enable", False, page.is_pricing_enable())
            self.verify("Tooltip for disabled Pricing displayed", True,
                        page.is_disabled_pricing_tool_tip_appears())

            page.switch_executable_status()
            time.sleep(1)
            self.verify("Is Executable enable", True, page.is_executable_enable())
            page.switch_pricing_status()
            time.sleep(1)
            self.verify("Is Pricing enable", True, page.is_pricing_enable())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
