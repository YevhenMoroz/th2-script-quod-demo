import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_800(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container, self.__class__.__name__)
        self.name_at_values_tab = "testName11"
        self.name_at_sub_counterparts = "data"
        self.party_id = "12"
        self.ext_id_client = "3"
        self.party_sub_id_type = "BIC"
        self.party_id_source = "BIC"
        self.venue_counterpart_id = "2"
        self.party_role = "Exchange"
        self.party_role_qualifier = "Bank"
        self.venue = "ANZ"

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
        counterparts_wizard.click_on_plus_sub_counterparts()
        counterparts_wizard.set_name_at_sub_counterparts_tab(self.name_at_sub_counterparts)
        counterparts_wizard.set_party_id_at_sub_counterparts_tab(self.party_id)
        counterparts_wizard.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client)
        counterparts_wizard.set_party_sub_id_at_sub_counterparts_tab(self.party_sub_id_type)
        counterparts_wizard.click_on_check_mark()
        time.sleep(2)
        counterparts_wizard.click_on_plus_party_roles()
        counterparts_wizard.set_party_id_source_at_party_roles_tab(self.party_id_source)
        counterparts_wizard.set_venue_counterpart_id_at_party_roles_tab(self.venue_counterpart_id)
        counterparts_wizard.set_party_role_at_party_roles_tab(self.party_role)
        counterparts_wizard.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client)
        counterparts_wizard.set_party_role_qualifier_at_party_roles_tab(self.party_role_qualifier)
        counterparts_wizard.set_venue_at_party_roles_tab(self.venue)
        counterparts_wizard.click_on_check_mark()
        time.sleep(3)

    def test_context(self):
        self.precondition()
        name = "newName"
        party_id = "new"
        ext_id_client = "new"
        party_sub_id_type = "Application"
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        list_of_set_sub_counterparts_value = [self.name_at_sub_counterparts,
                                              self.party_id,
                                              self.ext_id_client,
                                              self.party_sub_id_type]
        list_of_get_sub_counterparts_value = [counterparts_wizard.get_name_value_at_sub_counterparts_tab(),
                                              counterparts_wizard.get_party_id_value_at_sub_counterparts_tab(),
                                              counterparts_wizard.get_ext_id_client_value_at_sub_counterparts_tab(),
                                              counterparts_wizard.get_party_sub_id_type_value_at_sub_counterparts_tab()]
        fields_name_at_sub_counterparts = ["Name", "party id", "Ext ID", "Party Sub"]
        self.verify_arrays_of_data_objects("Sub counterparts before edit", fields_name_at_sub_counterparts,
                                           list_of_set_sub_counterparts_value, list_of_get_sub_counterparts_value)
        counterparts_wizard.click_on_edit_at_sub_counterparts_tab()
        counterparts_wizard.set_name_at_sub_counterparts_tab(name)
        counterparts_wizard.set_party_id_at_sub_counterparts_tab(party_id)
        counterparts_wizard.set_ext_id_client_at_sub_counterparts_tab(ext_id_client)
        counterparts_wizard.set_party_sub_id_at_sub_counterparts_tab(party_sub_id_type)
        counterparts_wizard.click_on_check_mark()
        list_of_new_set_sub_counterparts_values = [name, party_id, ext_id_client, party_sub_id_type]
        list_of_new_get_sub_counterparts_values = [counterparts_wizard.get_name_value_at_sub_counterparts_tab(),
                                                   counterparts_wizard.get_party_id_value_at_sub_counterparts_tab(),
                                                   counterparts_wizard.get_ext_id_client_value_at_sub_counterparts_tab(),
                                                   counterparts_wizard.get_party_sub_id_type_value_at_sub_counterparts_tab()]
        self.verify_arrays_of_data_objects("Sub counterparts after edit", fields_name_at_sub_counterparts,
                                           list_of_new_set_sub_counterparts_values,
                                           list_of_new_get_sub_counterparts_values)
        counterparts_wizard.click_on_save_changes()
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.set_name_filter_value(self.name_at_values_tab)
        time.sleep(2)
        self.verify("Counterparts main page", self.name_at_values_tab, counterparts_main_menu.get_name_value())
        time.sleep(2)
