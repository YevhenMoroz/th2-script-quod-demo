import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_802(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer,second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__,second_lvl_id)
        self.name = "zzz"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm07")
        login_page.set_password("adm07")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        time.sleep(2)
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.click_on_new()
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        counterparts_wizard.set_name_value_at_values_tab(self.name)
        counterparts_wizard.click_on_save_changes()
        counterparts_main_menu.click_on_more_actions()
        counterparts_main_menu.click_on_delete()
        time.sleep(1)
        counterparts_main_menu.click_on_cancel()
        time.sleep(1)
        counterparts_main_menu.set_name_filter_value(self.name)
        time.sleep(2)
        counterparts_main_menu.click_on_more_actions()
        counterparts_main_menu.click_on_delete()
        time.sleep(1)
        counterparts_main_menu.click_on_ok_xpath()

    def test_context(self):
        self.precondition()
        time.sleep(3)
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.set_name_filter_value(self.name)
        time.sleep(2)
        self.verify("After deleted", "TimeoutException",
                    counterparts_main_menu.check_that_name_value_row_is_not_exist())
