import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_description_sub_wizard import \
    ListingGroupsDescriptionSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_page import ListingGroupsPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_wizard import \
    ListingGroupsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_762(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sub_venue = 'Forward'
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listing_groups_page()
        time.sleep(2)
        page = ListingGroupsPage(self.web_driver_container)
        wizard = ListingGroupsWizard(self.web_driver_container)
        description_sub_wizard = ListingGroupsDescriptionSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(1)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_sub_venue(self.sub_venue)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        description_sub_wizard.set_name(self.new_name)

    def test_context(self):

        try:
            self.precondition()
            page = ListingGroupsPage(self.web_driver_container)
            wizard = ListingGroupsWizard(self.web_driver_container)
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name(self.new_name)
            time.sleep(2)
            self.verify("Is entity edited and  saved correctly and displayed in main page", self.new_name,
                        page.get_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
