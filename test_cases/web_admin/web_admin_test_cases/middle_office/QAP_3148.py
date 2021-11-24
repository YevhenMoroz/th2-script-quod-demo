import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard import \
    FeesCommissionProfilePointsSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_exec_fee_profile_sub_wizard import \
    FeesExecFeeProfileSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3148(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = 'PADM-499Descr'
        self.comm_xunit = 'Amount'
        self.comm_algorithm = 'Flat'
        self.base_value = '10'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_fees_page()
        page = FeesPage(self.web_driver_container)
        values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        exec_fee_profile_sub_wizard = FeesExecFeeProfileSubWizard(self.web_driver_container)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        wizard = FeesWizard(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard.click_on_manage_exec_fee_profile()
        time.sleep(2)
        exec_fee_profile_sub_wizard.click_on_plus()
        exec_fee_profile_sub_wizard.set_commission_profile_name(self.commission_profile_name)
        time.sleep(1)
        exec_fee_profile_sub_wizard.set_comm_xunit(self.comm_xunit)
        time.sleep(1)
        exec_fee_profile_sub_wizard.set_description(self.description)
        time.sleep(1)
        exec_fee_profile_sub_wizard.set_comm_algorithm(self.comm_algorithm)
        time.sleep(1)
        commission_profile_points.click_on_plus()
        time.sleep(2)
        commission_profile_points.set_base_value(self.base_value)
        time.sleep(2)
        commission_profile_points.click_on_checkmark()
        time.sleep(2)
        exec_fee_profile_sub_wizard.click_on_checkmark()
        time.sleep(2)
        wizard.click_on_go_back()
        time.sleep(2)
        values_sub_wizard.set_exec_fee_profile(self.commission_profile_name)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
            self.verify("whether the  Exec Fee Profile  was saved correctly", self.commission_profile_name,
                        values_sub_wizard.get_exec_fee_profile())
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
