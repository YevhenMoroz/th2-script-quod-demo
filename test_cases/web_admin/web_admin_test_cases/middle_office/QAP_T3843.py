import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.main_page import \
    SettlementModelsPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.values_sub_wizard import \
    SettlementModelsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.settlement_models.wizard import \
    SettlementModelsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3843(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.settl_location = self.data_set.get_settl_location("settl_location_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_settlement_models_page()
        time.sleep(2)
        page = SettlementModelsPage(self.web_driver_container)
        values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_settl_location(self.settl_location)

    def test_context(self):
        self.precondition()
        page = SettlementModelsPage(self.web_driver_container)
        wizard = SettlementModelsWizard(self.web_driver_container)
        excepted_pdf_values = [self.name,
                               self.description,
                               self.settl_location]

        self.verify("Is all data displayed correctly in PDF", True,
                    wizard.click_download_pdf_entity_button_and_check_pdf(excepted_pdf_values))

        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(1)
        try:
            self.verify("entity created correctly", self.name, page.get_name())

        except Exception as e:
            self.verify("entity not created", True, e.__class__.__name__)
