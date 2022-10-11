import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.couterparts_sub_counterparts_subwizard import \
    CounterpartsSubCounterpartsSubWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3291(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.party_id_source = ["BIC", "Proprietary"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        time.sleep(2)
        page = CounterpartsPage(self.web_driver_container)
        page.click_on_new()

    def test_context(self):
        subcounterparts_tab = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
        wizard = CounterpartsWizard(self.web_driver_container)

        try:
            self.precondition()

            wizard.click_on_plus_sub_counterparts()
            time.sleep(1)
            self.verify("Name field is required", True, subcounterparts_tab.is_name_field_required())
            self.verify("Party Id field is required", True, subcounterparts_tab.is_party_id_field_required())
            self.verify("Ext Id Client field is required", True, subcounterparts_tab.is_ext_id_client_field_required())
            self.verify("Party Sub Id field is required", True, subcounterparts_tab.is_party_sub_id_type_field_required())
            wizard.click_on_check_mark()
            time.sleep(1)
            self.verify("Empty entity not save", True, wizard.is_warning_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
