import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_dimensions_sub_wizard import FeesDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3448(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.misc_fee_type = 'Agent'
        self.venue_list = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_fees_page()

    def test_context(self):

        self.precondition()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        time.sleep(2)
        value_tab = FeesValuesSubWizard(self.web_driver_container)
        value_tab.set_description(self.description)
        value_tab.set_misc_fee_type(self.misc_fee_type)
        dimensions_tab = FeesDimensionsSubWizard(self.web_driver_container)
        self.venue_list = random.choice(dimensions_tab.get_all_venue_list_from_drop_menu())
        dimensions_tab.set_venue_list(self.venue_list)
        wizard = FeesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        fees_page.set_description(self.description)
        time.sleep(1)
        fees_page.click_on_more_actions()
        time.sleep(1)

        excepted_result = [self.description, self.misc_fee_type, self.venue_list]
        self.verify("PDF contains all data", True,
                    fees_page.click_download_pdf_entity_button_and_check_pdf(excepted_result))
