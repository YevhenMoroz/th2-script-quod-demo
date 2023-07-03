import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_dimensions_sub_wizard import FeesDimensionsSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3124(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.misk_fee_type = "Agent"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()

    def test_context(self):

        self.precondition()

        main_page = FeesPage(self.web_driver_container)
        main_page.click_on_new()

        values_tab = FeesValuesSubWizard(self.web_driver_container)
        values_tab.set_misc_fee_type(self.misk_fee_type)

        dimensions_tab = FeesDimensionsSubWizard(self.web_driver_container)
        available_route = dimensions_tab.get_all_route_from_drop_menu()
        excepted_result = set(available_route)

        self.verify("Value is present in list of routes and unique", len(available_route), len(excepted_result))
