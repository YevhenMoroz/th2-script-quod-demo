import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_dimensions_sub_wizard import \
    OrderVelocityLimitDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_page import \
    OrderVelocityLimitPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_values_sub_wizard import \
    OrderVelocityLimitValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_wizard import \
    OrderVelocityLimitWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5599(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.order_velocity_limit_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = '12'
        self.max_amount = '100000'
        self.max_quantity = '100000000'
        self.max_order_actions = '100000'

        self.side = 'Buy'
        self.client = 'CLIENT1'
        self.instr_symbol = 'AUD/HUF'
        self.new_client = 'CLIENT2'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_order_velocity_page()
        time.sleep(2)
        page = OrderVelocityLimitPage(self.web_driver_container)
        wizard = OrderVelocityLimitWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = OrderVelocityLimitValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_order_velocity_limit_name(self.order_velocity_limit_name)
        time.sleep(1)
        values_sub_wizard.set_moving_time_window(self.moving_time_window)
        time.sleep(1)
        values_sub_wizard.set_max_amount(self.max_amount)
        values_sub_wizard.set_max_quantity(self.max_quantity)
        values_sub_wizard.set_max_order_actions(self.max_order_actions)
        time.sleep(2)
        dimensions_sub_wizard = OrderVelocityLimitDimensionsSubWizard(self.web_driver_container)
        dimensions_sub_wizard.set_side(self.side)
        dimensions_sub_wizard.set_client(self.client)
        dimensions_sub_wizard.set_instr_symbol(self.instr_symbol)
        time.sleep(2)
        dimensions_sub_wizard.click_on_all_orders()
        time.sleep(2)
        dimensions_sub_wizard.click_on_all_orders()
        time.sleep(2)
        dimensions_sub_wizard.set_side(self.side)
        dimensions_sub_wizard.set_client(self.new_client)
        dimensions_sub_wizard.set_instr_symbol(self.instr_symbol)

    def test_context(self):

        try:
            self.precondition()
            page = OrderVelocityLimitPage(self.web_driver_container)
            wizard = OrderVelocityLimitWizard(self.web_driver_container)
            expected_pdf_content = [self.order_velocity_limit_name,
                                    self.moving_time_window,
                                    self.max_amount,
                                    self.max_quantity,
                                    self.max_order_actions,
                                    self.side,
                                    self.instr_symbol,
                                    self.new_client]
            self.verify("Is pdf contatins correctly values", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))

            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name(self.order_velocity_limit_name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            self.verify("Entity saved correctly", True, True)


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
