import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_general_sub_wizard import \
    ExecutionStrategiesGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_aggressive_sub_wizard import \
    ExecutionStrategiesLitAggressiveSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_general_sub_wizard import \
    ExecutionStrategiesLitGeneralSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_passive_sub_wizard import \
    ExecutionStrategiesLitPassiveSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_lit_sweeping_sub_wizard import \
    ExecutionStrategiesLitSweepingSubWizard
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_page import \
    ExecutionStrategiesPage
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_wizard import \
    ExecutionStrategiesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4272(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.strategy_type = "Quod MultiListing"
        self.user = "adm08"
        self.client = "CLIENT1"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_execution_strategies_page()
        time.sleep(1)
        # step 1
        execution_strategies_main_menu = ExecutionStrategiesPage(self.web_driver_container)
        execution_strategies_main_menu.click_on_new_button()
        # step 2
        execution_strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
        time.sleep(1)
        execution_strategies_wizard.set_name(self.name)
        time.sleep(1)
        execution_strategies_wizard.set_strategy_type(self.strategy_type)
        time.sleep(1)
        execution_strategies_wizard.set_client(self.client)
        # step 3
        execution_strategies_wizard.click_on_lit_passive()
        time.sleep(2)
        # step 4
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter("StatMarketShareCalcType")
        execution_strategies_lit_passive.set_value_by_dropdown_list_at_sub_wizard("Daily")
        execution_strategies_lit_passive.click_on_checkmark_button()
        # step 5
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter("PostMode")
        execution_strategies_lit_passive.set_value_by_dropdown_list_at_sub_wizard("Single")
        execution_strategies_lit_passive.click_on_checkmark_button()
        execution_strategies_lit_passive = ExecutionStrategiesLitPassiveSubWizard(self.web_driver_container)
        execution_strategies_lit_passive.click_on_plus_button()
        execution_strategies_lit_passive.set_parameter("StatMarketShareTimeHorizon")
        execution_strategies_lit_passive.set_value("22")
        execution_strategies_lit_passive.click_on_checkmark_button()
        # step 6
        execution_strategies_lit_passive.click_on_go_back_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            execution_strategies_main_menu = ExecutionStrategiesPage(self.web_driver_container)
            execution_strategies_wizard = ExecutionStrategiesWizard(self.web_driver_container)
            expected_parameter_and_value_at_lit_passive_block = [
                "StatMarketShareCalcType: ", "Daily"]
            actual_parameter_and_value_at_lit_passive_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_passive_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_passive_block()]
            self.verify("Check that new entity at lit passive saved correctly",
                        expected_parameter_and_value_at_lit_passive_block,
                        actual_parameter_and_value_at_lit_passive_block)
            # step 7
            # execution_strategies_wizard.click_on_general()
            # execution_strategies_general = ExecutionStrategiesGeneralSubWizard(self.web_driver_container)
            # execution_strategies_general.click_on_plus_button()
            # execution_strategies_general.set_parameter("SweepingPercentage")
            # execution_strategies_general.set_value_at_sub_wizard("33")
            # execution_strategies_general.click_on_checkmark_button()
            # execution_strategies_general.click_on_go_back_button()

            execution_strategies_wizard.click_on_lit_general()
            execution_strategies_lit_general = ExecutionStrategiesLitGeneralSubWizard(self.web_driver_container)
            execution_strategies_lit_general.click_on_plus_button()
            execution_strategies_lit_general.set_parameter("CrossCurrency")
            execution_strategies_lit_general.set_value_by_dropdown_list_at_sub_wizard("Default")
            execution_strategies_lit_general.click_on_checkmark_button()
            execution_strategies_lit_general.click_on_go_back_button()

            execution_strategies_wizard.click_on_lit_aggressive()
            execution_strategies_lit_aggressive = ExecutionStrategiesLitAggressiveSubWizard(self.web_driver_container)
            execution_strategies_lit_aggressive.click_on_plus_button()
            execution_strategies_lit_aggressive.set_parameter("StatHitRatioCalcType")
            execution_strategies_lit_aggressive.set_value_by_dropdown_list_at_sub_wizard("Daily")
            execution_strategies_lit_aggressive.click_on_checkmark_button()
            execution_strategies_lit_aggressive.click_on_go_back_button()

            execution_strategies_wizard.click_on_lit_sweeping()
            execution_strategies_lit_sweeping = ExecutionStrategiesLitSweepingSubWizard(self.web_driver_container)
            execution_strategies_lit_sweeping.click_on_plus_button()
            execution_strategies_lit_sweeping.set_parameter("MinimumPercentage")
            execution_strategies_lit_sweeping.set_value("12")
            execution_strategies_lit_sweeping.click_on_checkmark_button()
            execution_strategies_lit_sweeping.click_on_go_back_button()

            # step 8
            time.sleep(2)
            execution_strategies_wizard.click_on_save_changes()
            time.sleep(2)
            # step 9

            execution_strategies_main_menu.set_name_at_filter_field(self.name)
            time.sleep(2)
            execution_strategies_main_menu.click_on_more_actions()
            execution_strategies_main_menu.click_on_edit_at_more_actions()
            # expected_parameter_and_value_at_general_block = ["SweepingPercentage: ", "33"]
            # actual_parameter_and_value_at_general_block = [
            #     execution_strategies_wizard.get_parameter_name_at_general_block(),
            #     execution_strategies_wizard.get_parameter_value_at_general_block()]

            # self.verify("Check that values correctly saved  in General block after click on save changes button",
            #             expected_parameter_and_value_at_general_block,
            #             actual_parameter_and_value_at_general_block)

            expected_parameter_and_value_at_lit_general_block = ["CrossCurrency: ", "Default"]
            actual_parameter_and_value_at_lit_general_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_general_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_general_block()]

            self.verify("Check that values correctly saved  in Lit General block after click on save changes button",
                        expected_parameter_and_value_at_lit_general_block,
                        actual_parameter_and_value_at_lit_general_block)

            expected_parameter_and_value_at_lit_aggressive_block = ["StatHitRatioCalcType: ", "Daily"]
            actual_parameter_and_value_at_lit_aggressive_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_aggressive_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_aggressive_block()]

            self.verify("Check that values correctly saved  in Lit Aggressive block after click on save changes button",
                        expected_parameter_and_value_at_lit_aggressive_block,
                        actual_parameter_and_value_at_lit_aggressive_block)

            expected_parameter_and_value_at_sweeping_block = ["MinimumPercentage: ", "12"]
            actual_parameter_and_value_at_sweeping_block = [
                execution_strategies_wizard.get_parameter_name_at_lit_sweeping_block(),
                execution_strategies_wizard.get_parameter_value_at_lit_sweeping_block()]

            self.verify("Check that values correctly saved  in Lit Sweeping block after click on save changes button",
                        expected_parameter_and_value_at_sweeping_block,
                        actual_parameter_and_value_at_sweeping_block)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
