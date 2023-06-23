import random
import string
import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
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


class QAP_T3839(CommonTestCase):

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
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settlement_models_page()
        time.sleep(2)
        page = SettlementModelsPage(self.web_driver_container)
        values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
        wizard = SettlementModelsWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_settl_location(self.settl_location)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        page = SettlementModelsPage(self.web_driver_container)
        page.set_name(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        time.sleep(1)
        page.click_on_delete(True)
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_info_error_message_pop_up()
        common_page.click_on_user_icon()
        time.sleep(1)
        common_page.click_on_logout()
        time.sleep(2)
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_settlement_models_page()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(1)
        self.verify("Entity is deleted", False, page.is_searched_entity_found(self.name))

