import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from test_framework.web_admin_core.pages.others.counterparts.couterparts_sub_counterparts_subwizard \
    import CounterpartsSubCounterpartsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8930(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.sub_counterparts_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.party_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.party_sub_id_type = 'BIC'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()

        main_page = CounterpartsPage(self.web_driver_container)
        main_page.click_on_new()
        wizard = CounterpartsWizard(self.web_driver_container)
        wizard.set_name_value_at_values_tab(self.name)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            main_page = CounterpartsPage(self.web_driver_container)
            main_page.set_name_filter_value(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            wizard = CounterpartsWizard(self.web_driver_container)
            wizard.click_on_plus_sub_counterparts()
            sub_counterparts_wizard = CounterpartsSubCounterpartsSubWizard(self.web_driver_container)
            sub_counterparts_wizard.set_name_at_sub_counterparts_tab(self.sub_counterparts_name)
            sub_counterparts_wizard.set_party_id_at_sub_counterparts_tab(self.party_id)
            sub_counterparts_wizard.set_ext_id_client_at_sub_counterparts_tab(self.ext_id_client)
            sub_counterparts_wizard.set_party_sub_id_at_sub_counterparts_tab(self.party_sub_id_type)
            wizard.click_on_check_mark()
            wizard.click_on_save_changes()

            main_page.set_name_filter_value(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            wizard.click_on_edit_at_sub_counterparts_tab()
            actual_result = [sub_counterparts_wizard.get_name_value_at_sub_counterparts_tab(),
                             sub_counterparts_wizard.get_party_id_value_at_sub_counterparts_tab(),
                             sub_counterparts_wizard.get_ext_id_client_value_at_sub_counterparts_tab(),
                             sub_counterparts_wizard.get_party_sub_id_type_value_at_sub_counterparts_tab()]

            expected_result = [self.sub_counterparts_name, self.party_id, self.ext_id_client, self.party_sub_id_type]

            self.verify('Sub-counterparts create correct', actual_result, expected_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
