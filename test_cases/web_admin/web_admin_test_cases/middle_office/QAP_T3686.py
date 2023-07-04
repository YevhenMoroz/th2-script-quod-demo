import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_dimensions_sub_wizard import FeesDimensionsSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3686(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.misc_fee_type = 'ExchFees'
        self.country_of_issue = 'ALA'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_fees_page()
        page = FeesPage(self.web_driver_container)
        values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        wizard = FeesWizard(self.web_driver_container)
        dimensions_tab = FeesDimensionsSubWizard(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard.set_misc_fee_type(self.misc_fee_type)
        time.sleep(2)
        dimensions_tab.set_country_of_issue(self.country_of_issue)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    def test_context(self):

        self.precondition()
        dimensions_tab = FeesDimensionsSubWizard(self.web_driver_container)
        self.verify("whether the  Exec Fee Profile  was saved correctly", self.country_of_issue,
                    dimensions_tab.get_country_of_issue())
