import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_page import \
    QuotingSessionsPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_values_sub_wizard import \
    QuotingSessionsValuesSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_wizard import \
    QuotingSessionsWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3519(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''
        self.concurrently_active_quotes_age = ["", str(random.randint(100, 500))]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_quoting_sessions_page()

    def test_context(self):
        wizard = QuotingSessionsWizard(self.web_driver_container)
        page = QuotingSessionsPage(self.web_driver_container)
        value_tab = QuotingSessionsValuesSubWizard(self.web_driver_container)

        try:
            self.precondition()

            page.click_on_more_actions()
            page.click_on_edit()

            self.name = value_tab.get_name()
            self.verify("Is 'Concurrently Active Quote Age' field required", True,
                        value_tab.is_concurrently_active_quotes_age_required())
            value_tab.set_concurrently_active_quotes_age(self.concurrently_active_quotes_age[0])

            wizard.click_on_save_changes()

            self.verify("Entity not save, error message appears", True, wizard.is_warning_in_footer_displayed())
            value_tab.set_concurrently_active_quotes_age(self.concurrently_active_quotes_age[1])
            wizard.click_on_save_changes()

            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            self.verify("'Concurrently Active Quote Age' has been changed", self.concurrently_active_quotes_age[1],
                        value_tab.get_concurrently_active_quotes())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
