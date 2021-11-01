import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_page import SubVenuesPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_wizard import SubVenuesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_758(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMEX"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_subvenues_page()
        time.sleep(2)
        page = SubVenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        time.sleep(2)
        description_sub_wizard.set_venue(self.venue)
        time.sleep(2)
        wizard = SubVenuesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = SubVenuesPage(self.web_driver_container)
            page.click_on_delete(True)
            self.verify("Entity deleted correctly", True, True)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
