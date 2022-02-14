import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_cases.web_admin.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard import \
    CounterpartsPartyRolesSubWizard
from test_cases.web_admin.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard

from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_6314(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.party_role = "GiveupClearingFirm"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_counterparts_page()
        time.sleep(2)
        page = CounterpartsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        wizard = CounterpartsWizard(self.web_driver_container)
        wizard.click_on_plus_party_roles()

    def test_context(self):
        try:
            self.precondition()
            party_roles_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
            try:
                party_roles_wizard.set_party_role_at_party_roles_tab(self.party_role)
                self.verify(f"Party Role contains {self.party_role}", True, True)
            except Exception as e:
                self.verify(f"Party Role contains {self.party_role}", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
