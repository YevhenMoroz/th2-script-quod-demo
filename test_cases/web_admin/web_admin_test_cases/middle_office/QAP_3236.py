import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_commision_profiles_sub_wizard import \
    CommissionsCommissionProfilesSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_commission_profile_points_sub_wizard import \
    CommissionsCommissionProfilePointsSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard import \
    CommissionsDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard import \
    CommissionsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3236(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"

        # Dimensions tab

        self.instr_type = "Bond"
        self.venue = "BINANCE"
        self.side = "Buy"
        self.execution_policy = "DMA"
        # self.virtual_account = "TEST"
        # self.client = "ASCBank"
        # self.client_group = "DEMO"
        self.client_list = "WEILRG"
        self.commission_amount_type = "Broker"
        # self.commission_profile = "UK stamp"

        # Values tab
        self.commission_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(1)
        dimensions_tab.set_instr_type(self.instr_type)
        time.sleep(1)
        dimensions_tab.set_venue(self.venue)
        time.sleep(1)
        dimensions_tab.set_side(self.side)
        time.sleep(1)
        dimensions_tab.set_execution_policy(self.execution_policy)
        time.sleep(1)
        # dimensions_tab.set_virtual_account(self.virtual_account)
        # time.sleep(1)
        # dimensions_tab.set_client(self.client)
        # time.sleep(1)
        # dimensions_tab.set_client_group(self.client_group)
        time.sleep(1)
        dimensions_tab.set_client_list(self.client_list)
        time.sleep(1)
        dimensions_tab.set_commission_amount_type(self.commission_amount_type)
        time.sleep(1)
        values_tab = CommissionsValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.commission_name)
        time.sleep(1)
        values_tab.set_description(self.description)
        time.sleep(1)
        wizard = CommissionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            wizard = CommissionsWizard(self.web_driver_container)
            dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
            page = CommissionsPage(self.web_driver_container)
            page.set_name(self.commission_name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            expected_pdf = [self.instr_type,
                            self.venue,
                            self.side,
                            self.execution_policy,
                            # self.virtual_account,
                            # self.client,
                            # self.client_group,
                            self.client_list,
                            self.commission_amount_type,
                            # self.commission_profile,
                            self.commission_name,
                            self.description

                            ]
            self.verify("Is PDF contains saved entity", True,
                        page.click_download_pdf_entity_button_and_check_pdf(expected_pdf))


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
