import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard import \
    CounterpartsPartyRolesSubWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3834(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name_at_values_tab = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name_at_sub_counterparts = "data"
        self.party_id = "12"
        self.ext_id_client = "3"
        self.party_sub_id_type = "BIC"
        self.party_id_source = "BIC"
        self.venue_counterpart_id = "ClientLEI"+''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.party_role = self.data_set.get_party_role("party_role_1")
        self.party_role_qualifier = "Bank"
        self.venue = self.data_set.get_venue_by_name("venue_1")
        ######
        self.new_party_id_source = "MIC"
        self.new_venue_counterpart_id = "14"
        self.new_party_role = "DeskID"
        self.new_ext_id_client = "2"
        self.new_party_role_qualifier = "Current"
        self.new_venue = self.data_set.get_venue_by_name("venue_5")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
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
        time.sleep(1)
        wizard = CounterpartsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
        time.sleep(1)
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        wizard = CounterpartsWizard(self.web_driver_container)
        counterparts_main_menu.click_on_more_actions()
        time.sleep(1)
        counterparts_main_menu.click_on_edit()
        time.sleep(2)
        wizard.click_on_edit_at_party_roles_tab()
        time.sleep(1)
        party_roles_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
        party_roles_wizard.set_party_id_source_at_party_roles_tab(self.new_party_id_source)
        party_roles_wizard.set_venue_counterpart_id_at_party_roles_tab(self.new_venue_counterpart_id)
        party_roles_wizard.set_party_role_at_party_roles_tab(self.new_party_role)
        party_roles_wizard.set_ext_id_client_at_party_roles_tab(self.new_ext_id_client)
        party_roles_wizard.set_party_role_qualifier_at_party_roles_tab(self.new_party_role_qualifier)
        party_roles_wizard.set_venue_at_party_roles_tab(self.new_venue)
        counterparts_wizard.click_on_check_mark()
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
        time.sleep(2)
        expected_pdf_result = [self.new_party_id_source,
                               self.new_venue_counterpart_id,
                               self.new_party_role,
                               self.new_ext_id_client,
                               self.new_party_role_qualifier,
                               self.new_venue]

        self.verify("Is party roles tab edited correctly", True,
                    counterparts_main_menu.click_download_pdf_at_more_actions_and_check_pdf(expected_pdf_result))
