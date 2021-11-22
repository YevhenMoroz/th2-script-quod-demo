import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_wizard import \
    CumTradingLimitsWizard
from quod_qa.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_dimensions_sub_wizard import \
    TradingLimitsDimensionsSubWizardPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_page import TradingLimitsPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_values_sub_wizard import \
    TradingLimitsValuesSubWizardPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_780(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.external_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = "EUR"
        self.max_quantity = "10"
        self.max_amount = "7"
        self.user = "adm07"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_trading_limits_page()
        time.sleep(2)
        main_page = TradingLimitsPage(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(2)
        values_sub_wizard = TradingLimitsValuesSubWizardPage(self.web_driver_container)
        values_sub_wizard.set_description(self.description)
        time.sleep(1)
        values_sub_wizard.set_external_id(self.external_id)
        time.sleep(1)
        values_sub_wizard.set_currency(self.currency)
        time.sleep(1)
        values_sub_wizard.set_max_quantity(self.max_quantity)
        time.sleep(1)
        values_sub_wizard.set_max_amount(self.max_amount)
        time.sleep(1)
        dimensions_sub_wizard = TradingLimitsDimensionsSubWizardPage(self.web_driver_container)
        dimensions_sub_wizard.set_user(self.user)
        time.sleep(1)
        wizard = CumTradingLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(1)

    def test_context(self):

        try:
            self.precondition()
            main_page = TradingLimitsPage(self.web_driver_container)
            main_page.set_description(self.description)
            values_sub_wizard = TradingLimitsValuesSubWizardPage(self.web_driver_container)
            time.sleep(2)
            main_page.click_on_more_actions()
            time.sleep(2)
            main_page.click_on_edit()
            time.sleep(2)
            self.verify("Is new trading limit saved correctly", self.description, values_sub_wizard.get_description())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
