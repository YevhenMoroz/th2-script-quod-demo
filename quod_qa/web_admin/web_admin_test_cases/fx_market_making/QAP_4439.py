import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_instruments_sub_wizard import \
    AutoHedgerInstrumentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instrument_wizard import \
    ClientTierInstrumentWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_page import ClientTiersPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4439(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.strategy = "Default"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        time.sleep(2)
        page = AutoHedgerPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            instruments_sub_wizard = AutoHedgerInstrumentsSubWizard(self.web_driver_container)
            instruments_sub_wizard.click_on_plus_button()
            try:
                instruments_sub_wizard.set_hedging_execution_strategy(self.strategy)
                self.verify("Default strategy selected correctly", True, True)

            except Exception as e:
                self.verify("Default strategy", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
