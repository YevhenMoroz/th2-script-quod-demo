import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_exec_fee_profile_sub_wizard \
    import FeesExecFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard \
    import FeesCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8857(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.exec_scope = ['AllExec', 'DayFirstExec', 'FirstExec', 'OnCalculated']
        self.comm_type = ['AbsoluteAmount', 'PerUnit']
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.commission_profile_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                        for _ in range(2)]
        self.comm_xunit = 'Quantity'
        self.comm_algorithm = 'Flat'
        self.base_values = '1 '
        self.misc_fee_type = ['Other', 'Agent']

    def create_new_exec_fee_profile(self, name, comm_type, comm_xunit, comm_algorithm, base_value):
        exec_fee_profile = FeesExecFeeProfileSubWizard(self.web_driver_container)
        exec_fee_profile.click_on_plus()
        exec_fee_profile.set_commission_profile_name(name)
        exec_fee_profile.set_comm_type(comm_type)
        exec_fee_profile.set_comm_xunit(comm_xunit)
        exec_fee_profile.set_comm_algorithm(comm_algorithm)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        commission_profile_points.set_base_value(base_value)
        commission_profile_points.click_on_checkmark()
        exec_fee_profile.click_on_checkmark()

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        values_tab = FeesValuesSubWizard(self.web_driver_container)
        values_tab.click_on_manage_exec_fee_profile()

        self.create_new_exec_fee_profile(self.commission_profile_name[0], self.comm_type[0], self.comm_xunit,
                                         self.comm_algorithm, self.base_values)
        self.create_new_exec_fee_profile(self.commission_profile_name[1], self.comm_type[1], self.comm_xunit,
                                         self.comm_algorithm, self.base_values)

        wizard = FeesWizard(self.web_driver_container)
        wizard.click_on_go_back()

    def test_context(self):
        fees_page = FeesPage(self.web_driver_container)
        values_tab = FeesValuesSubWizard(self.web_driver_container)
        wizard = FeesWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            values_tab.set_misc_fee_type(self.misc_fee_type[0])
            values_tab.set_exec_scope(self.exec_scope[0])
            values_tab.set_exec_fee_profile(self.commission_profile_name[0])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = AllExec, CommType = Absolute", True,
                        common_act.is_error_message_displayed())

            values_tab.set_exec_scope(self.exec_scope[3])
            values_tab.set_exec_fee_profile(self.commission_profile_name[0])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = OnCalculated, CommType = Absolute", True,
                        common_act.is_error_message_displayed())

            values_tab.set_exec_scope(self.exec_scope[0])
            values_tab.set_exec_fee_profile(self.commission_profile_name[1])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = AllExec, CommType = PerUnit", True,
                        common_act.is_error_message_displayed())

            values_tab.set_exec_scope(self.exec_scope[3])
            values_tab.set_exec_fee_profile(self.commission_profile_name[1])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = OnCalculated, CommType = PerUnit", True,
                        common_act.is_error_message_displayed())

            values_tab.set_exec_scope(self.exec_scope[2])
            values_tab.set_exec_fee_profile(self.commission_profile_name[0])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = FirstExec, CommType = Absolute", True,
                        common_act.is_error_message_displayed())

            values_tab.set_exec_scope(self.exec_scope[1])
            values_tab.set_exec_fee_profile(self.commission_profile_name[0])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Exec Scope = DayFirstExec, CommType = Absolute", True,
                        common_act.is_error_message_displayed())

            values_tab.set_misc_fee_type(self.misc_fee_type[1])
            values_tab.set_exec_scope('')
            values_tab.set_exec_fee_profile(self.commission_profile_name[1])
            wizard.click_on_save_changes()
            time.sleep(1)
            self.verify("Fees is not saved. Misc Fee Type = Agent, CommType = PerUnit", True,
                        common_act.is_error_message_displayed())

            values_tab.set_description(self.description)
            values_tab.set_exec_scope(self.exec_scope[2])
            values_tab.set_exec_fee_profile(self.commission_profile_name[0])
            wizard.click_on_save_changes()
            fees_page.set_description(self.description)
            time.sleep(1)
            self.verify("Fees saved. Exec Scope = FirstExec, CommType = Absolute", True,
                        fees_page.is_searched_entity_found(self.description))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
