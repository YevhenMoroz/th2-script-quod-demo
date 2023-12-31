import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards \
    import MainWizard, ValuesTab, DimensionsTab
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3339(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.position_limits = list
        self.desk = "DESK A"
        self.account_dimensions = "Clients"
        self.client = "CLIENT1"
        self.user_dimension = "Desks"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_risk_limit_dimension_page()
        time.sleep(2)

    def post_conditions(self):
        main_page = MainPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):
        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            time.sleep(2)
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name)
            time.sleep(1)
            self.position_limits = values_tab.get_all_position_limits_from_drop_menu()
            values_tab.set_cum_trading_limits([random.choice(self.position_limits)])

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_accounts_dimension(self.account_dimensions)
            time.sleep(1)
            dimensions_tab.set_clients([self.client])
            time.sleep(1)
            dimensions_tab.set_users_dimension(self.user_dimension)
            time.sleep(1)
            dimensions_tab.set_desks([self.desk])

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name_filter(self.name)
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found(self.name))

            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)

            self.verify("Diemensions tab has no Position Limits field", False,
                        values_tab.is_position_limit_field_displayed())

            wizard.click_on_close()
            time.sleep(2)

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
