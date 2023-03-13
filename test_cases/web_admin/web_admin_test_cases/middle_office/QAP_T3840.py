import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.dimensions_sub_wizard import \
    SettlementModelsDimensionsSubWizard
from test_framework.web_admin_core.pages.middle_office.settlement_models.main_page import \
    SettlementModelsPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.values_sub_wizard import \
    SettlementModelsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.settlement_models.wizard import \
    SettlementModelsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3840(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.settl_location = self.data_set.get_settl_location("settl_location_1")
        self.settl_location_bic = "test"
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.country_code = self.data_set.get_country_code("country_code_1")
        self.client_group = self.data_set.get_client_group("client_group_1")
        self.account = "DEMO_MO1"
        self.client = self.data_set.get_client("client_1")
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.instrument = self.data_set.get_instrument("instrument_2")
        self.instrument_group = self.data_set.get_instrument_group("instrument_group_1")

        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_settl_location = self.data_set.get_settl_location("settl_location_2")
        self.new_settl_location_bic = "test2"
        self.new_instr_type = self.data_set.get_instr_type("instr_type_8")
        self.new_country_code = self.data_set.get_country_code("country_code_2")
        self.new_client_group = self.data_set.get_client_group("client_group_2")
        self.new_account = "DEMO_MO2"
        self.new_client = self.data_set.get_client("client_2")
        self.new_venue = self.data_set.get_venue_by_name("venue_6")
        self.new_instrument = self.data_set.get_instrument("instrument_1")
        self.new_instrument_group = self.data_set.get_instrument_group("instrument_group_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_settlement_models_page()
        time.sleep(2)
        page = SettlementModelsPage(self.web_driver_container)
        values_sub_wizard = SettlementModelsValuesSubWizard(self.web_driver_container)
        dimensions_sub_wizard = SettlementModelsDimensionsSubWizard(self.web_driver_container)
        wizard = SettlementModelsWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        time.sleep(1)
        values_sub_wizard.set_description(self.description)
        values_sub_wizard.set_settl_location(self.settl_location)
        values_sub_wizard.set_settl_location_bic(self.settl_location_bic)
        values_sub_wizard.set_instr_type(self.instr_type)
        values_sub_wizard.set_country_code(self.country_code)
        dimensions_sub_wizard.set_client_group(self.client_group)
        dimensions_sub_wizard.set_account(self.account)
        dimensions_sub_wizard.set_client(self.client)
        dimensions_sub_wizard.set_venue(self.venue)
        dimensions_sub_wizard.set_instrument_group(self.instrument_group)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard.set_name(self.new_name)
        values_sub_wizard.set_description(self.new_description)
        values_sub_wizard.set_settl_location(self.new_settl_location)
        values_sub_wizard.set_settl_location_bic(self.new_settl_location_bic)
        values_sub_wizard.set_instr_type(self.new_instr_type)
        values_sub_wizard.set_country_code(self.new_country_code)
        dimensions_sub_wizard.set_client_group(self.new_client_group)
        dimensions_sub_wizard.set_account(self.new_account)
        dimensions_sub_wizard.set_client(self.new_client)
        dimensions_sub_wizard.set_venue(self.new_venue)
        dimensions_sub_wizard.set_instrument_group(self.new_instrument_group)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.new_name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = SettlementModelsPage(self.web_driver_container)
            excepted_pdf_values = [self.new_name,
                                   self.new_description,
                                   self.new_settl_location,
                                   self.new_settl_location_bic,
                                   self.new_instr_type,
                                   self.new_country_code,
                                   self.new_client_group,
                                   self.new_account,
                                   self.new_client,
                                   self.new_venue,
                                   self.new_instrument_group
                                   ]

            self.verify("Is all data displayed correctly in PDF", True,
                        page.click_download_pdf_entity_button_and_check_pdf(excepted_pdf_values))


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
