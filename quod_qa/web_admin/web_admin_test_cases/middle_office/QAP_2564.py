import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard import \
    CommissionsDimensionsSubWizard
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard import \
    CommissionsValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2564(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = "description"
        self.instr_type = 'Bond'
        self.venue = 'EURONEXT AMSTERDAM'
        self.side = 'Buy'
        self.execution_policy = 'Care'
        self.client = 'CLIENT1'
        self.commission_amount_type = 'Broker'
        self.commission_profile = '1bps'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
        values_tab = CommissionsValuesSubWizard(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(1)
        dimensions_tab.set_instr_type(self.instr_type)
        dimensions_tab.set_venue(self.venue)
        dimensions_tab.set_side(self.side)
        dimensions_tab.set_execution_policy(self.execution_policy)
        dimensions_tab.set_client(self.client)
        dimensions_tab.set_commission_amount_type(self.commission_amount_type)
        dimensions_tab.set_commission_profile(self.commission_profile)
        values_tab.set_name(self.name)
        values_tab.set_description(self.description)

    def test_context(self):

        try:
            self.precondition()
            wizard = CommissionsWizard(self.web_driver_container)
            main_page = CommissionsPage(self.web_driver_container)
            expected_pdf_result = [self.name,
                                   self.description,
                                   self.instr_type,
                                   self.venue,
                                   self.side,
                                   self.execution_policy,
                                   self.client,
                                   self.commission_amount_type,
                                   self.commission_profile]
            self.verify("Is pdf contains correctly values", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_result))

            wizard.click_on_save_changes()
            time.sleep(2)
            try:
                main_page.set_name(self.name)
                time.sleep(2)
                main_page.click_on_more_actions()
                self.verify("Entity saved correctly", True, True)
            except Exception as e:
                self.verify("Entity did not save !!!Error!!!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
