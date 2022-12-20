import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard \
    import CommissionsValuesSubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9132(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.commission_amount_type = ['Unspecified', 'Acceptance', 'Broker', 'ClearingBroker', 'Retail',
                                       'SalesCommission', 'LocalCommission', 'ResearchPayment']
        self.actual_com_amt_type = str
        self.commission_amount_sub_type = ['ResearchPaymentAccount', 'CommissionSharingAgreement', 'Other']
        self.actual_com_amt_sub_type = str

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_commissions_page()

        commission_page = CommissionsPage(self.web_driver_container)
        commission_page.click_on_new()
        value_tab = CommissionsValuesSubWizard(self.web_driver_container)
        value_tab.set_name(self.name)
        value_tab.set_description(self.description)
        value_tab.set_commission_amount_type(random.choice(value_tab.get_all_commission_amount_type_from_drop_menu()))
        wizard = CommissionsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):

        try:
            self.precondition()

            commission_page = CommissionsPage(self.web_driver_container)
            commission_page.set_name(self.name)
            time.sleep(1)
            commission_page.click_on_more_actions()
            commission_page.click_on_edit()

            value_tab = CommissionsValuesSubWizard(self.web_driver_container)
            
            self.actual_com_amt_type = value_tab.get_all_commission_amount_type_from_drop_menu()
            self.verify("Commission amount type contains preconditions values", sorted(self.commission_amount_type),
                        sorted(self.actual_com_amt_type))

            self.actual_com_amt_sub_type = value_tab.get_all_commission_amount_sub_type_from_drop_menu()
            self.verify("Commission amount sub type contains preconditions values",
                        sorted(self.commission_amount_sub_type),
                        sorted(self.actual_com_amt_sub_type))
            com_amt_type = random.choice(self.actual_com_amt_type)
            value_tab.set_commission_amount_type(com_amt_type)
            com_amt_sub_type = random.choice(self.actual_com_amt_sub_type)
            value_tab.set_commission_amount_sub_type(com_amt_sub_type)

            wizard = CommissionsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            commission_page.set_name(self.name)
            time.sleep(1)
            commission_page.click_on_more_actions()
            commission_page.click_on_edit()

            actual_result = [value_tab.get_commission_amount_type(), value_tab.get_commission_amount_sub_type()]
            expected_result = [com_amt_type, com_amt_sub_type]

            self.verify("Commission saved", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
