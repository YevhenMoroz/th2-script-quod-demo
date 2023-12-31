import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards \
    import MainWizard, ValuesTab, DimensionsTab, AssignmentsTab

from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_page import TradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_wizard import TradingLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_assignments_sub_wizard \
    import TradingLimitsAssignmentsSubWizardPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_values_sub_wizard \
    import TradingLimitsValuesSubWizardPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_dimensions_sub_wizard \
    import TradingLimitsDimensionsSubWizardPage

from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_page \
    import CumTradingLimitsPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_wizard \
    import CumTradingLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_dimensions_sub_wizard \
    import CumTradingLimitsDimensionsSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_values_sub_wizard \
    import CumTradingLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_assignments_sub_wizard \
    import CumTradingLimitsAssignmentsSubWizard

from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_page import PositionLimitsPage
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_values_sub_wizard \
    import PositionLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_wizard import PositionLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_assignments_sub_wizard \
    import PositionLimitsAssignmentsSubWizardPage

from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.main_page \
    import OrderToleranceLimitsPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.wizard \
    import OrderToleranceLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.values_sub_wizard \
    import OrderToleranceLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.assignments_sub_wizard \
    import OrderToleranceLimitsAssignmentsSubWizardPage

from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.main_page import \
    OrderVelocityLimitsPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.values_sub_wizard import \
    OrderVelocityLimitsValuesSubWizard
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.wizard import \
    OrderVelocityLimitsWizard
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.assignment_tab import \
    OrderVelocityLimitsAssignmentsSubWizardPage

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3204(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.user_dimension = "Desks"
        self.desk = "DESK A"
        self.institution = "QUOD FINANCIAL"
        self.external_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.moving_time_window = str(random.randint(0, 10))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def risk_limits_dimension_page(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_risk_limit_dimension_page()

        risk_limit_dimension_page = MainPage(self.web_driver_container)
        risk_limit_dimension_page.click_on_new_button()
        values_tab = ValuesTab(self.web_driver_container)
        values_tab.set_name(self.name)

        dimensions_tab = DimensionsTab(self.web_driver_container)
        dimensions_tab.set_users_dimension(self.user_dimension)
        dimensions_tab.set_desks(self.desk)

        assignments_tab = AssignmentsTab(self.web_driver_container)
        assignments_tab.set_institution(self.institution)

        wizard = MainWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        risk_limit_dimension_page.set_name_filter(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    risk_limit_dimension_page.is_searched_entity_found(self.name))

        risk_limit_dimension_page.click_on_more_actions()
        risk_limit_dimension_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        risk_limit_dimension_page.set_name_filter(self.name)
        time.sleep(1)
        risk_limit_dimension_page.click_on_more_actions()
        risk_limit_dimension_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        risk_limit_dimension_page.set_name_filter(self.name)
        time.sleep(1)
        risk_limit_dimension_page.click_on_more_actions()
        risk_limit_dimension_page.click_on_delete(True)
        risk_limit_dimension_page.set_name_filter(self.name)
        time.sleep(1)
        self.verify("Risk Limit Dimension entity deleted", False,
                    risk_limit_dimension_page.is_searched_entity_found(self.name))

    def trading_limits_page(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_trading_limits_page()
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        trading_limits_page = TradingLimitsPage(self.web_driver_container)
        trading_limits_page.click_on_new()

        values_tab = TradingLimitsValuesSubWizardPage(self.web_driver_container)
        values_tab.set_description(self.name)
        dimensions_tab = TradingLimitsDimensionsSubWizardPage(self.web_driver_container)
        dimensions_tab.set_desk(self.desk)
        assignments_tab = TradingLimitsAssignmentsSubWizardPage(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard = TradingLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        trading_limits_page.set_description(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    trading_limits_page.is_searched_entity_found_by_description(self.name))

        trading_limits_page.click_on_more_actions()
        trading_limits_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        trading_limits_page.set_description(self.name)
        time.sleep(1)
        trading_limits_page.click_on_more_actions()
        trading_limits_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        trading_limits_page.set_description(self.name)
        time.sleep(1)
        trading_limits_page.click_on_more_actions()
        trading_limits_page.click_on_delete(True)
        trading_limits_page.set_description(self.name)
        time.sleep(1)
        self.verify("Trading Limit entity deleted", False,
                    trading_limits_page.is_searched_entity_found_by_description(self.name))

    def cum_trading_limits(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_cum_trading_limits_page()
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        cum_trading_page = CumTradingLimitsPage(self.web_driver_container)
        cum_trading_page.click_on_new()
        value_tab = CumTradingLimitsValuesSubWizard(self.web_driver_container)
        value_tab.set_description(self.name)
        dimensions_tab = CumTradingLimitsDimensionsSubWizard(self.web_driver_container)
        dimensions_tab.set_desk(self.desk)
        assignments_tab = CumTradingLimitsAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard = CumTradingLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        cum_trading_page.set_description(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    cum_trading_page.is_searched_cum_trading_limits_found(self.name))

        cum_trading_page.click_on_more_actions()
        cum_trading_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        cum_trading_page.set_description(self.name)
        time.sleep(1)
        cum_trading_page.click_on_more_actions()
        cum_trading_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        cum_trading_page.set_description(self.name)
        time.sleep(1)
        cum_trading_page.click_on_more_actions()
        cum_trading_page.click_on_delete(True)
        cum_trading_page.set_description(self.name)
        time.sleep(1)
        self.verify("Cum Trading Limits entity deleted", False,
                    cum_trading_page.is_searched_cum_trading_limits_found(self.name))

    def position_limits(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_positions_limits_page()
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        position_limits_page = PositionLimitsPage(self.web_driver_container)
        position_limits_page.click_on_new()
        value_tab = PositionLimitsValuesSubWizard(self.web_driver_container)
        value_tab.set_description(self.name)

        assignments_tab = PositionLimitsAssignmentsSubWizardPage(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard = PositionLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        position_limits_page.set_description(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    position_limits_page.is_searched_entity_found(self.name))

        position_limits_page.click_on_more_actions()
        position_limits_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        position_limits_page.set_description(self.name)
        time.sleep(1)
        position_limits_page.click_on_more_actions()
        position_limits_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        position_limits_page.set_description(self.name)
        time.sleep(1)
        position_limits_page.click_on_more_actions()
        position_limits_page.click_on_delete(True)
        position_limits_page.set_description(self.name)
        time.sleep(1)
        self.verify("Position Limits entity deleted", False,
                    position_limits_page.is_searched_entity_found(self.name))

    def price_tolerance_control(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_tolerance_limits_page()
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        price_tolerance_page = OrderToleranceLimitsPage(self.web_driver_container)
        price_tolerance_page.click_on_new()
        value_tab = OrderToleranceLimitsValuesSubWizard(self.web_driver_container)
        value_tab.set_name(self.name)
        value_tab.set_external_id(self.external_id)

        assignments_tab = OrderToleranceLimitsAssignmentsSubWizardPage(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard = OrderToleranceLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        price_tolerance_page.set_name(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    price_tolerance_page.is_searched_entity_found_by_name(self.name))

        price_tolerance_page.click_on_more_actions()
        price_tolerance_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        price_tolerance_page.set_name(self.name)
        time.sleep(1)
        price_tolerance_page.click_on_more_actions()
        price_tolerance_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        price_tolerance_page.set_name(self.name)
        time.sleep(1)
        price_tolerance_page.click_on_more_actions()
        price_tolerance_page.click_on_delete(True)
        price_tolerance_page.set_name(self.name)
        time.sleep(1)
        self.verify("Price Tolerance Control entity deleted", False,
                    price_tolerance_page.is_searched_entity_found_by_name(self.name))

    def order_velocity_limits(self):
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_velocity_page()
        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        order_velocity_limit_page = OrderVelocityLimitsPage(self.web_driver_container)
        order_velocity_limit_page.click_on_new()

        values_sub_wizard = OrderVelocityLimitsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_order_velocity_limit_name(self.name)
        values_sub_wizard.set_moving_time_window(self.moving_time_window)

        assignments_tab = OrderVelocityLimitsAssignmentsSubWizardPage(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        wizard = OrderVelocityLimitsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        order_velocity_limit_page.set_name(self.name)
        time.sleep(1)
        self.verify("New entity has been create", True,
                    order_velocity_limit_page.is_searched_entity_found_by_name(self.name))

        order_velocity_limit_page.click_on_more_actions()
        order_velocity_limit_page.click_on_edit()

        assignments_tab.clear_institution_field()

        wizard.click_on_save_changes()

        order_velocity_limit_page.set_name(self.name)
        time.sleep(1)
        order_velocity_limit_page.click_on_more_actions()
        order_velocity_limit_page.click_on_edit()
        actual_result = False if self.institution in assignments_tab.get_institution() else True
        self.verify("Institutions has been cleared", True, actual_result)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_info_error_message_pop_up()
        wizard.click_on_revert_changes()
        wizard.click_on_close()

        order_velocity_limit_page.set_name(self.name)
        time.sleep(1)
        order_velocity_limit_page.click_on_more_actions()
        order_velocity_limit_page.click_on_delete(True)
        order_velocity_limit_page.set_name(self.name)
        time.sleep(1)
        self.verify("Order Velocity Limits entity deleted", False,
                    order_velocity_limit_page.is_searched_entity_found_by_name(self.name))

    def test_context(self):
        try:
            self.precondition()

            self.risk_limits_dimension_page()
            self.trading_limits_page()
            self.cum_trading_limits()
            self.position_limits()
            time.sleep(2)
            self.price_tolerance_control()
            time.sleep(2)
            self.order_velocity_limits()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
