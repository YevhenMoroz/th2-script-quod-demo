import sys
import time
import traceback
import string
import random

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_values_sub_wizard \
    import AutoHedgerValuesSubWizard
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_wizard import AutoHedgerWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8497(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.positions_book = 'ACABankFirm'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_auto_hedger_page()

    def test_context(self):
        try:
            self.precondition()

            page = AutoHedgerPage(self.web_driver_container)
            page.click_on_new()

            values_tab = AutoHedgerValuesSubWizard(self.web_driver_container)
            values_tab.set_name(self.name)
            values_tab.set_position_book(self.positions_book)

            wizard = AutoHedgerWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            page.set_name_filter(self.name)
            time.sleep(1)
            self.verify("MultiListing type available", True, page.is_auto_hedger_found_by_name(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
