import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard import \
    CounterpartsPartyRolesSubWizard
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.couterparts_sub_counterparts_subwizard import \
    CounterpartsSubCounterpartsSubWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_676(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
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
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_counterparts_page()
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        time.sleep(2)
        counterparts_main_menu.click_on_new()
        time.sleep(1)
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        time.sleep(1)
        counterparts_wizard.set_name_value_at_values_tab(self.name_at_values_tab)
        time.sleep(2)
        counterparts_wizard.click_on_plus_sub_counterparts()
        sub_counterparts_wizard = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
        sub_counterparts_wizard.set_name_at_sub_counterparts_tab(self.name_at_sub_counterparts)
        sub_counterparts_wizard.set_party_id_at_sub_counterparts_tab(self.party_id)
        sub_counterparts_wizard.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client)
        sub_counterparts_wizard.set_party_sub_id_at_sub_counterparts_tab(self.party_sub_id_type)
        time.sleep(2)
        counterparts_wizard.click_on_check_mark()
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
        counterparts_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()
            sub_counterparts_wizard = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
            counterparts_wizard = CounterpartsWizard(self.web_driver_container)
            counterparts_main_menu = CounterpartsPage(self.web_driver_container)
            party_roles_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
            time.sleep(2)
            counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
            time.sleep(2)
            counterparts_main_menu.click_on_more_actions()
            time.sleep(1)
            counterparts_main_menu.click_on_edit()
            self.verify("Is field Name saved correctly", self.name_at_values_tab,
                        counterparts_wizard.get_name_at_values_tab())
            time.sleep(1)
            list_of_set_sub_counterparts_value = [self.name_at_sub_counterparts,
                                                  self.party_id,
                                                  self.ext_id_client,
                                                  self.party_sub_id_type]
            list_of_get_sub_counterparts_value = [sub_counterparts_wizard.get_name_value_at_sub_counterparts_tab(),
                                                  sub_counterparts_wizard.get_party_id_value_at_sub_counterparts_tab(),
                                                  sub_counterparts_wizard.get_ext_id_client_value_at_sub_counterparts_tab(),
                                                  sub_counterparts_wizard.get_party_sub_id_type_value_at_sub_counterparts_tab()]
            time.sleep(1)
            fields_name_at_sub_counterparts = ["Name", "party id", "Ext ID", "Party Sub"]
            self.verify_arrays_of_data_objects("Is Sub counterparts saved correctly", fields_name_at_sub_counterparts,
                                               list_of_set_sub_counterparts_value, list_of_get_sub_counterparts_value)

            list_of_set_party_roles_value = [self.party_id_source,
                                             self.venue_counterpart_id,
                                             self.party_role,
                                             self.ext_id_client,
                                             self.party_role_qualifier,
                                             self.venue]

            list_of_get_party_roles_value = [party_roles_wizard.get_party_id_source_value_at_party_roles_tab(),
                                             party_roles_wizard.get_venue_counterpart_id_value_at_party_roles_tab(),
                                             party_roles_wizard.get_party_role_value_at_party_roles_tab(),
                                             party_roles_wizard.get_ext_id_client_value_at_party_roles_tab(),
                                             party_roles_wizard.get_party_role_qualifier_value_at_party_roles_tab(),
                                             party_roles_wizard.get_venue_value_at_party_roles_tab()]

            fields_name_at_party_roles = ["Party ID Source", "Venue Counterpart ID", "Party Role", "Ext ID Client",
                                          "Party Role Qualifier", "Venue"]
            self.verify_arrays_of_data_objects("Is party roles saved correctly", fields_name_at_party_roles,
                                               list_of_set_party_roles_value, list_of_get_party_roles_value)
            time.sleep(2)
            counterparts_wizard.click_on_save_changes()
            time.sleep(2)
            counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
            time.sleep(2)
            counterparts_main_menu.click_on_more_actions()
            time.sleep(1)
            counterparts_main_menu.click_on_delete_and_confirmation(True)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)

