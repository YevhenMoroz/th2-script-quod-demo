import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard import \
    InstitutionsValuesSubWizard
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3306(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.cash_account_currency_rate_source = ['ManualRate', 'MarketRate']
        self.cross_currency_hair_cut = ['2', '3']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_institutions_page()

        page = InstitutionsPage(self.web_driver_container)
        page.click_on_new()

        values_tab = InstitutionsValuesSubWizard(self.web_driver_container)
        values_tab.click_at_cross_currency_settlement_checkbox()
        time.sleep(1)
        values_tab.set_cash_account_currency_rate_source(self.cash_account_currency_rate_source[0])
        values_tab.set_cross_currency_hair_cut(self.cross_currency_hair_cut[0])
        values_tab.set_institution_name(self.name)

        wizard = InstitutionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

        page.set_institution_name(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_edit()

    def test_context(self):
        try:
            self.precondition()

            values_tab = InstitutionsValuesSubWizard(self.web_driver_container)
            values_tab.set_cash_account_currency_rate_source(self.cash_account_currency_rate_source[1])
            values_tab.set_cross_currency_hair_cut(self.cross_currency_hair_cut[1])

            wizard = InstitutionsWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            page = InstitutionsPage(self.web_driver_container)
            page.set_institution_name(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            expected_result = [self.cross_currency_hair_cut[1], self.cash_account_currency_rate_source[1]]
            actual_result = [values_tab.get_cross_currency_hair_cut(),
                             values_tab.get_cash_account_currency_rate_source()]

            self.verify("New data saved", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
