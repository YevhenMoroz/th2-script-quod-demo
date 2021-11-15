import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_page import RoutesPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_venues_subwizard import RoutesVenuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5816(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.user_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.mic = "ALXP"
        self.venue = "ADX"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_routes_page()
        routes_page = RoutesPage(self.web_driver_container)
        routes_page.click_on_new_button()
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            routes_venues_sub_wizard = RoutesVenuesSubWizard(self.web_driver_container)
            routes_venues_sub_wizard.click_on_plus_at_venues_tab()
            routes_venues_sub_wizard.set_venue_at_venues_tab(self.venue)
            routes_venues_sub_wizard.set_mic_at_venues_tab_at_venues_tab(self.mic)
            routes_venues_sub_wizard.click_on_check_mark_at_venues_tab()
            self.verify("Mic at venue created correctly", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
