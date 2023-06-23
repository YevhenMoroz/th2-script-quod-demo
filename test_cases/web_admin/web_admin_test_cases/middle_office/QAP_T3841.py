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


class QAP_T3841(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.settl_location = self.data_set.get_settl_location("settl_location_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settlement_models_page()
        time.sleep(2)
        page = SettlementModelsPage(self.web_driver_container)
        wizard = SettlementModelsWizard(self.web_driver_container)
        values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_settl_location(self.settl_location)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        time.sleep(1)
        page.click_on_clone()
        time.sleep(1)
        values_sub_wizard.set_name(self.new_name)

    def test_context(self):
        self.precondition()
        page = SettlementModelsPage(self.web_driver_container)
        wizard = SettlementModelsWizard(self.web_driver_container)
        values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
        excepted_values_after_click_on_clone_button = [
            self.description,
            self.settl_location]
        actual_values_after_click_on_clone_button = [values_sub_wizard.get_description(),
                                                     values_sub_wizard.get_settl_location()]

        self.verify("Clone entity contains parent data", excepted_values_after_click_on_clone_button,
                    actual_values_after_click_on_clone_button)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        try:
            self.verify("Is PDF contains correct values", True, page.click_download_pdf_entity_button_and_check_pdf(
                excepted_values_after_click_on_clone_button))
        except Exception as e:
            self.verify("PDF result is incorrect", True, e.__class__.__name__)
