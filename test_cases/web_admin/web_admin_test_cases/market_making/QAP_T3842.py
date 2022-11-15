import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3842(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.core_spot_price_strategy = ["MidPoint", "TopOfBook", "VWAPPriceOptimized", "VWAPSpeedOptimized"]
        self.tod_end_time = "23:59:59"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_main_page = ClientTiersPage(self.web_driver_container)
        client_tiers_main_page.click_on_more_actions()
        client_tiers_main_page.click_on_edit()

    def test_context(self):
        try:
            self.precondition()

            client_tier_wizard_value_tab = ClientTiersValuesSubWizard(self.web_driver_container)
            client_tier_wizard_value_tab.set_tod_end_time(self.tod_end_time)
            client_tier_wizard_value_tab.clear_field_core_spot_price_strategy()
            time.sleep(1)
            core_spot_price_items = client_tier_wizard_value_tab.get_all_core_spot_price_strategy_from_drop_menu()
            actual_result = [True if self.core_spot_price_strategy[i] in core_spot_price_items else False
                             for i in range(len(self.core_spot_price_strategy))]
            excepted_result = [True for _ in range(len(self.core_spot_price_strategy))]

            self.verify("Core spot price strategy contains test data", excepted_result, actual_result)

            new_core_spot_price_strategy = random.choice(self.core_spot_price_strategy)
            client_tier_wizard_value_tab.set_core_spot_price_strategy(new_core_spot_price_strategy)
            client_tier_wizard = ClientTiersWizard(self.web_driver_container)
            edited_client_tier = client_tier_wizard_value_tab.get_name()
            client_tier_wizard.click_on_save_changes()
            client_tiers_main_page = ClientTiersPage(self.web_driver_container)
            client_tiers_main_page.set_client_tiers_global_filter(edited_client_tier)
            time.sleep(1)
            client_tiers_main_page.click_on_more_actions()
            client_tiers_main_page.click_on_edit()

            self.verify("New Core Spot Price Strategy was save correctly", new_core_spot_price_strategy,
                        client_tier_wizard_value_tab.get_core_spot_price_strategy())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
