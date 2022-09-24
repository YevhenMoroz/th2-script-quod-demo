import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.couterparts_sub_counterparts_subwizard \
    import CounterpartsSubCounterpartsSubWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard \
    import CounterpartsPartyRolesSubWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3888(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name_at_values_tab = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name_at_value_tab = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.name_at_sub_counterparts = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                         for _ in range(2)]
        self.party_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.ext_id_client_at_sub_counterparts = [
            ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
            for _ in range(2)]
        self.party_sub_id_type = ["BIC", "Firm"]

        self.party_id_source = ["ISO", "MIC"]
        self.venue_counterpart_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                     for _ in range(2)]
        self.party_role = [self.data_set.get_party_role("party_role_1"), self.data_set.get_party_role("party_role_2")]
        self.ext_id_client_at_party_role = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                            for _ in range(2)]
        self.party_role_qualifier = ["Bank", "Current"]
        self.venue = [self.data_set.get_venue_by_name("venue_1"), self.data_set.get_venue_by_name("venue_2")]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        counterparts_page = CounterpartsPage(self.web_driver_container)
        counterparts_page.click_on_new()

        wizard = CounterpartsWizard(self.web_driver_container)
        wizard.set_name_value_at_values_tab(self.name_at_values_tab)
        wizard.click_on_plus_sub_counterparts()
        sub_counterparts_tab = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
        sub_counterparts_tab.set_name_at_sub_counterparts_tab(self.name_at_sub_counterparts[0])
        sub_counterparts_tab.set_party_id_at_sub_counterparts_tab(self.party_id[0])
        sub_counterparts_tab.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client_at_sub_counterparts[0])
        sub_counterparts_tab.set_party_sub_id_at_sub_counterparts_tab(self.party_sub_id_type[0])
        wizard.click_on_check_mark()

        wizard.click_on_plus_party_roles()
        party_roles_tab = CounterpartsPartyRolesSubWizard(self.web_driver_container)
        party_roles_tab.set_party_id_source_at_party_roles_tab(self.party_id_source[0])
        party_roles_tab.set_venue_counterpart_id_at_party_roles_tab(self.venue_counterpart_id[0])
        party_roles_tab.set_party_role_at_party_roles_tab(self.party_role[0])
        party_roles_tab.set_ext_id_client_at_party_roles_tab(self.ext_id_client_at_party_role[0])
        party_roles_tab.set_party_role_qualifier_at_party_roles_tab(self.party_role_qualifier[0])
        party_roles_tab.set_venue_at_party_roles_tab(self.venue[0])
        wizard.click_on_check_mark()

        wizard.click_on_save_changes()
        counterparts_page.set_name_filter_value(self.name_at_values_tab)
        time.sleep(1)

    def post_conditions(self):
        counterparts_page = CounterpartsPage(self.web_driver_container)
        counterparts_page.set_name_filter_value(self.new_name_at_value_tab)
        time.sleep(1)
        counterparts_page.click_on_more_actions()
        counterparts_page.click_on_delete_and_confirmation(True)

    def test_context(self):

        try:
            self.precondition()

            counterparts_page = CounterpartsPage(self.web_driver_container)
            counterparts_page.click_on_more_actions()
            counterparts_page.click_on_edit()

            wizard = CounterpartsWizard(self.web_driver_container)
            wizard.set_name_value_at_values_tab(self.new_name_at_value_tab)

            wizard.click_on_edit_at_sub_counterparts_tab()
            sub_counterparts_tab = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
            sub_counterparts_tab.set_name_at_sub_counterparts_tab(self.name_at_sub_counterparts[1])
            sub_counterparts_tab.set_party_id_at_sub_counterparts_tab(self.party_id[1])
            sub_counterparts_tab.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client_at_sub_counterparts[1])
            sub_counterparts_tab.set_party_sub_id_at_sub_counterparts_tab(self.party_sub_id_type[1])
            wizard.click_on_check_mark()

            wizard.click_on_edit_at_party_roles_tab()
            party_roles_tab = CounterpartsPartyRolesSubWizard(self.web_driver_container)
            party_roles_tab.set_party_id_source_at_party_roles_tab(self.party_id_source[1])
            party_roles_tab.set_venue_counterpart_id_at_party_roles_tab(self.venue_counterpart_id[1])
            party_roles_tab.set_party_role_at_party_roles_tab(self.party_role[1])
            party_roles_tab.set_ext_id_client_at_party_roles_tab(self.ext_id_client_at_party_role[1])
            party_roles_tab.set_party_role_qualifier_at_party_roles_tab(self.party_role_qualifier[1])
            party_roles_tab.set_venue_at_party_roles_tab(self.venue[1])
            wizard.click_on_check_mark()
            wizard.click_on_save_changes()

            counterparts_page.set_name_filter_value(self.new_name_at_value_tab)
            time.sleep(1)
            counterparts_page.click_on_more_actions()
            counterparts_page.click_on_edit()

            actual_result = [wizard.get_name_at_values_tab(),
                             sub_counterparts_tab.get_name_value_at_sub_counterparts_tab(),
                             sub_counterparts_tab.get_party_id_value_at_sub_counterparts_tab(),
                             sub_counterparts_tab.get_ext_id_client_value_at_sub_counterparts_tab(),
                             sub_counterparts_tab.get_party_sub_id_type_value_at_sub_counterparts_tab(),
                             party_roles_tab.get_party_id_source_value_at_party_roles_tab(),
                             party_roles_tab.get_venue_counterpart_id_value_at_party_roles_tab(),
                             party_roles_tab.get_party_role_value_at_party_roles_tab(),
                             party_roles_tab.get_ext_id_client_value_at_party_roles_tab(),
                             party_roles_tab.get_party_role_qualifier_value_at_party_roles_tab(),
                             party_roles_tab.get_venue_value_at_party_roles_tab()]
            excepted_result = [self.new_name_at_value_tab, self.name_at_sub_counterparts[1], self.party_id[1],
                               self.ext_id_client_at_sub_counterparts[1], self.party_sub_id_type[1],
                               self.party_id_source[1], self.venue_counterpart_id[1], self.party_role[1],
                               self.ext_id_client_at_party_role[1], self.party_role_qualifier[1], self.venue[1]]

            self.verify("Edit data saved correctly", excepted_result, actual_result)

            wizard.click_on_save_changes()

            self.post_conditions()


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
