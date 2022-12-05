import random
import sys
import traceback
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.main_page \
    import OrderVelocityLimitsPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.values_sub_wizard \
    import OrderVelocityLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.dimensions_sub_wizard \
    import OrderVelocityLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.assignment_tab \
    import OrderVelocityLimitsAssignmentsSubWizardPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.wizard \
    import OrderVelocityLimitsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7931(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.fields_name = ["Moving Time Window", "Max Amount", "Max Order Actions", "Max Quantity", "Auto Reset",
                            "Client", "Side", "Instr Symbol", "Listing", "All Orders", "Institution"]
        self.max_amount = str(random.randint(1, 100))
        self.institution = 'QUOD FINANCIAL'
        self.client = 'CLIENT2'
        self.instr_symbol = 'AUD/HUF'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_velocity_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = OrderVelocityLimitsPage(self.web_driver_container)
            main_page.click_on_new()

            wizard = OrderVelocityLimitsWizard(self.web_driver_container)

            self.verify("PDF contains all fields name", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.fields_name))

            values_tab = OrderVelocityLimitsValuesSubWizard(self.web_driver_container)
            values_tab.set_order_velocity_limit_name(self.name)
            values_tab.set_max_amount(self.max_amount)

            assignments_tab = OrderVelocityLimitsAssignmentsSubWizardPage(self.web_driver_container)
            assignments_tab.set_institution(self.institution)

            dimensions_tab = OrderVelocityLimitsDimensionsSubWizard(self.web_driver_container)
            dimensions_tab.set_client(self.client)
            dimensions_tab.set_instr_symbol(self.instr_symbol)

            self.verify("PDF contains all fields name", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.fields_name))
            actual_result = [self.name, self.max_amount, self.institution, self.client, self.instr_symbol]
            self.verify("PDF contains all values field", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(actual_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
