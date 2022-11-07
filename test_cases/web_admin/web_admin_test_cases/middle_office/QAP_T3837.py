import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
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


class QAP_T3837(CommonTestCase):

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
        side_menu.open_settlement_models_page()
        page = SettlementModelsPage(self.web_driver_container)
        page.click_on_new()

    def test_context(self):
        try:
            self.precondition()

            exception_message = "Incorrect or missing values"
            values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
            wizard = SettlementModelsWizard(self.web_driver_container)
            values_sub_wizard.set_name(self.name)
            wizard.click_on_save_changes()
            self.verify("Entity with only name not save", exception_message,
                        wizard.get_incorrect_or_missing_values_exception())

            self.verify("Is name field mandatory (using check in DOM)", True,
                        values_sub_wizard.is_name_field_required())
            self.verify("Is description field mandatory (using check in DOM)", True,
                        values_sub_wizard.is_description_field_required())
            self.verify("Is settl_location field mandatory (using check in DOM)", True,
                        values_sub_wizard.is_settl_location_field_required())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
