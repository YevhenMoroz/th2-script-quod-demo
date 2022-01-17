import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_external_sources_sub_wizard import \
    ClientsExternalSourcesSubWizard
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_cases.web_admin.web_admin_core.pages.client_accounts.clients.clients_wizard import ClientsWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3230(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.venue_act_group_name_bic = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_clients_page()
        time.sleep(2)
        page = ClientsPage(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        external_sources_sub_wizard = ClientsExternalSourcesSubWizard(self.web_driver_container)
        external_sources_sub_wizard.set_bic_venue_act_grp_name(self.venue_act_group_name_bic)
        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()

    def test_context(self):
        try:
            self.precondition()
            external_sources_sub_wizard = ClientsExternalSourcesSubWizard(self.web_driver_container)
            self.verify("Is bic venue act group name saved correctly", self.venue_act_group_name_bic,
                        external_sources_sub_wizard.get_bic_venue_act_grp_name())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
