import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_page import \
    QuotingSessionsPage
from quod_qa.web_admin.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_values_sub_wizard import \
    QuotingSessionsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_wizard import \
    QuotingSessionsWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1757(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.published_quote_id_format = "#20d"
        self.quote_update_format = "FullRefresh"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_quoting_sessions_page()
        page = QuotingSessionsPage(self.web_driver_container)
        wizard = QuotingSessionsWizard(self.web_driver_container)
        values_sub_wizard = QuotingSessionsValuesSubWizard(self.web_driver_container)
        time.sleep(1)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_published_quote_id_format(self.published_quote_id_format)
        time.sleep(1)
        values_sub_wizard.set_quote_update_format(self.quote_update_format)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_user_icon()
        time.sleep(2)
        page.click_on_logout()
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu.open_quoting_sessions_page()
        time.sleep(1)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            values_sub_wizard = QuotingSessionsValuesSubWizard(self.web_driver_container)
            expected_result_values = [self.name,
                                      self.published_quote_id_format,
                                      self.quote_update_format,
                                      ]
            actual_result_values = [values_sub_wizard.get_name(),
                                    values_sub_wizard.get_published_quote_id_format(),
                                    values_sub_wizard.get_quote_update_format()]
            self.verify("Check is entity created correctly", expected_result_values,
                        actual_result_values)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
