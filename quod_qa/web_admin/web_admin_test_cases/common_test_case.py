from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommonTestCase:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container

    def run(self):
        try:
            self.__start_driver()
            self.test_context()
        except Exception:
            print("An error was occurred during the test case execution!")
        finally:
            self.__stop_driver()

    # @abc.abstractmethod
    def test_context(self):
        # raise NotImplementedError("Please implement this method!")
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm04")
        login_page.set_password("adm04")
        login_page.click_login_button()
        login_page.check_is_login_successful()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

        accounts_page = AccountsPage(self.web_driver_container)
        accounts_page.filter_grid("A0")
        accounts_page.click_more_actions_button()
        print(accounts_page.click_download_pdf_entity_button_and_check_pdf("Description: Virtual account for Broker account group"))

    def __start_driver(self):
        self.web_driver_container.start_driver()

    def __stop_driver(self):
        self.web_driver_container.stop_driver()

