import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard \
    import CommissionsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard \
    import CommissionsDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3446(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_list = ''
        self.commission_amount_type = 'Broker'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()

    def test_context(self):

        try:
            self.precondition()
            commission_page = CommissionsPage(self.web_driver_container)
            commission_page.click_on_new()
            time.sleep(2)
            value_tab = CommissionsValuesSubWizard(self.web_driver_container)
            value_tab.set_name(self.name)
            value_tab.set_description(self.description)
            value_tab.set_commission_amount_type(self.commission_amount_type)
            dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
            self.venue_list = random.choice(dimensions_tab.get_all_venue_list_from_drop_menu())
            dimensions_tab.set_venue_list(self.venue_list)
            wizard = CommissionsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            commission_page.set_name(self.name)
            time.sleep(1)
            commission_page.click_on_more_actions()
            time.sleep(1)

            excepted_result = [self.name, self.description, self.venue_list, self.commission_amount_type]
            self.verify("PDF contains all data", True,
                        commission_page.click_download_pdf_entity_button_and_check_pdf(excepted_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
