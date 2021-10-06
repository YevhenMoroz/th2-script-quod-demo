import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_wizard import AutoHedgerWizard

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2772(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm03"
        self.password = "adm03"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()
        main_page = AutoHedgerPage(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            wizard = AutoHedgerWizard(self.web_driver_container)
            expected_pdf_content = ["External Clients", "Internal Clients", "Instruments"]
            self.verify("Pdf contains correctly value", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
