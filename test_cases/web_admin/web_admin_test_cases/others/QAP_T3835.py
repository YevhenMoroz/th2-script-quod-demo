import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard \
    import CounterpartsPartyRolesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3835(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.party_rule_table = {key: ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                 for key in ["venue_counterpart_id", "ext_id_client"]}
        self.party_rule_table.update({"party_id_source": "LegalEntityIdentifier", "party_role": "ClientID"})

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.click_on_new()
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        counterparts_wizard.set_name_value_at_values_tab(self.name)

        counterparts_wizard.click_on_plus_party_roles()
        counterparts_sub_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
        counterparts_sub_wizard.set_party_id_source_at_party_roles_tab(self.party_rule_table["party_id_source"])
        counterparts_sub_wizard.set_venue_counterpart_id_at_party_roles_tab(self.party_rule_table["venue_counterpart_id"])
        counterparts_sub_wizard.set_party_role_at_party_roles_tab(self.party_rule_table["party_role"])
        counterparts_sub_wizard.set_ext_id_client_at_party_roles_tab(self.party_rule_table["ext_id_client"])
        counterparts_wizard.click_on_check_mark()
        counterparts_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            counterparts_main_menu = CounterpartsPage(self.web_driver_container)
            counterparts_main_menu.set_name_filter_value(self.name)
            time.sleep(1)
            self.verify("Counterpart entity is create", "True",
                        counterparts_main_menu.is_counterpart_present_by_name(self.name))
            time.sleep(1)
            expected_result = [_ for _ in self.party_rule_table.values()]
            expected_result.append(self.name)
            self.verify("PDF file contains test data", "True",
                        counterparts_main_menu.click_download_pdf_at_more_actions_and_check_pdf(expected_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
