import random
import string
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


class QAP_3229(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.name_at_values_tab = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name_at_sub_counterparts = "data"
        self.party_id = "12"
        self.ext_id_client = "3"
        self.party_sub_id_type = "BIC"
        self.party_id_source = "BIC"
        self.venue_counterpart_id = "2"
        self.party_role = "Exchange"
        self.party_role_qualifier = "Bank"
        self.venue = "AMEX"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        time.sleep(2)
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.click_on_new()
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        time.sleep(1)
        counterparts_wizard.set_name_value_at_values_tab(self.name_at_values_tab)
        time.sleep(2)
        counterparts_wizard.click_on_plus_party_roles()
        party_roles_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
        party_roles_wizard.set_party_id_source_at_party_roles_tab(self.party_id_source)
        party_roles_wizard.set_venue_counterpart_id_at_party_roles_tab(self.venue_counterpart_id)
        party_roles_wizard.set_party_role_at_party_roles_tab(self.party_role)
        party_roles_wizard.set_ext_id_client_at_party_roles_tab(self.ext_id_client)
        party_roles_wizard.set_party_role_qualifier_at_party_roles_tab(self.party_role_qualifier)
        party_roles_wizard.set_venue_at_party_roles_tab(self.venue)
        counterparts_wizard.click_on_check_mark()
        time.sleep(3)
        wizard = CounterpartsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            counterparts_main_menu = CounterpartsPage(self.web_driver_container)
            counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
            wizard = CounterpartsWizard(self.web_driver_container)
            time.sleep(2)
            counterparts_main_menu.click_on_more_actions()
            time.sleep(2)
            counterparts_main_menu.click_on_edit()
            time.sleep(2)
            wizard.click_on_delete_at_party_roles_tab()
            time.sleep(2)
            try:
                wizard.click_on_edit_at_party_roles_tab()
                self.verify("entity at party roles NOT deleted", True, False)
            except Exception:
                self.verify("entity at party roles deleted", True, True)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
