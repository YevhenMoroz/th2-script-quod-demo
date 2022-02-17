import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.settlement_model.settlement_model_page import \
    SettlementModelPage
from test_cases.web_admin.web_admin_core.pages.middle_office.settlement_model.settlement_model_values_sub_wizard import \
    SettlementModelValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.settlement_model.settlement_model_wizard import \
    SettlementModelWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3223(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.settl_location = 'CASH'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_settlement_model_page()
        time.sleep(2)
        page = SettlementModelPage(self.web_driver_container)
        values_sub_wizard = SettlementModelValuesSubWizard(self.web_driver_container)
        wizard = SettlementModelWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(1)
        values_sub_wizard.set_name(self.name)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_settl_location(self.settl_location)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = SettlementModelPage(self.web_driver_container)
            page.set_name(self.name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            page.click_on_delete(True)
            time.sleep(15)
            common_page = CommonPage(self.web_driver_container)
            common_page.click_on_user_icon()
            time.sleep(2)
            common_page.click_on_logout()
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.login, self.password)
            side_menu = SideMenu(self.web_driver_container)
            time.sleep(2)
            side_menu.open_settlement_model_page()
            time.sleep(2)
            try:
                page.set_name(self.name)
                time.sleep(2)
                page.click_on_more_actions()
                self.verify("entity  is not deleted correctly", False, "entity is exist after deleting")
            except Exception:
                self.verify("entity deleted", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
