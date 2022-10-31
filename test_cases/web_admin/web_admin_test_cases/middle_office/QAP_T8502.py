import sys
import string
import random
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_dimensions_sub_wizard import FeesDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8502(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.misc_fee_type = ''
        self.except_misc_fee_type = ['Agent', 'ValueAddedTax']
        self.client_list = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()

    def test_context(self):

        try:
            self.precondition()

            main_page = FeesPage(self.web_driver_container)
            main_page.click_on_new()

            values_tab = FeesValuesSubWizard(self.web_driver_container)
            values_tab.set_description(self.description)
            self.misc_fee_type = values_tab.get_all_misc_fee_type_from_drop_menu()
            [self.misc_fee_type.pop(self.misc_fee_type.index(i)) for i in self.except_misc_fee_type]
            self.misc_fee_type = random.choice(self.misc_fee_type)
            values_tab.set_misc_fee_type(self.misc_fee_type)

            dimensions_tab = FeesDimensionsSubWizard(self.web_driver_container)
            self.client_list = random.choice(dimensions_tab.get_all_client_list_from_drop_menu())
            dimensions_tab.set_client_list(self.client_list)

            wizard = FeesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_description(self.description)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            self.verify("ClientList saved", self.client_list, dimensions_tab.get_client_list())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
