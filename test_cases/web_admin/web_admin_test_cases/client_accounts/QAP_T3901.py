import time
import string
import random

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard \
    import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_external_sources_sub_wizard \
    import ClientsExternalSourcesSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3901(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T3901'
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_bic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk = self.data_set.get_desk("desk_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        main_page = ClientsPage(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)
        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
        assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_clients_page()
        main_page.set_name(self.name)
        time.sleep(1)

        if not main_page.is_searched_client_found(self.name):
            main_page.click_on_new()
            values_tab.set_id(self.id)
            values_tab.set_name(self.name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab.set_desk(self.desk)
            wizard.click_on_save_changes()
            main_page.set_name(self.name)
            time.sleep(1)
        else:
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            external_source_tab.set_bic_venue_act_grp_name("")
            wizard.click_on_save_changes()
            main_page.set_name(self.name)
            time.sleep(1)

        main_page.click_on_more_actions()
        main_page.click_on_edit()

    def test_context(self):
        main_page = ClientsPage(self.web_driver_container)
        external_source_tab = ClientsExternalSourcesSubWizard(self.web_driver_container)
        wizard = ClientsWizard(self.web_driver_container)

        self.precondition()

        external_source_tab.set_bic_venue_act_grp_name(self.bic)
        wizard.click_on_save_changes()
        time.sleep(1)
        main_page.set_name(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_edit()

        self.verify("BIC has value", self.bic, external_source_tab.get_bic_venue_act_grp_name())

        external_source_tab.set_bic_venue_act_grp_name(self.new_bic)
        wizard.click_on_save_changes()
        main_page.set_name(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_edit()

        self.verify("BIC has been changed", self.new_bic, external_source_tab.get_bic_venue_act_grp_name())

        external_source_tab.set_bic_venue_act_grp_name("")
        wizard.click_on_save_changes()
        main_page.set_name(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_edit()
        actual_result = True if len(external_source_tab.get_bic_venue_act_grp_name()) > 1 else False
        self.verify("BIC has not values", True, actual_result)
