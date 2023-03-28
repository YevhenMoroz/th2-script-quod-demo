from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_constant import LoginConstants
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3425(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login1 = self.data_set.get_user("user_1")
        self.login3 = self.data_set.get_user("user_3")
        self.password1 = self.data_set.get_password("password_1")

        self.client1_1 = self.data_set.get_client("client1_1")
        self.client1_2 = self.data_set.get_client("client1_2")
        self.client1_3 = self.data_set.get_client("client1_3")
        self.client2_1 = self.data_set.get_client("client2_1")
        self.client2_2 = self.data_set.get_client("client2_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login1, self.password1)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # region - test details

        # Step 1
        main_page.click_on_menu()
        menu_page.click_on_preferences()
        self.verify("Step 1 - Preferences is opened", None, menu_page.wait_element_presence(MenuConstants.PREFERENCES_TITLE))
        self.verify("Step 1 - Default Client title is shown", None, menu_page.wait_element_presence(MenuConstants.DEFAULT_CLIENT_TITLE))
        self.verify("Step 1 - Default Client dropdown is shown", None, menu_page.wait_element_presence(MenuConstants.DEFAULT_CLIENT_DROP_DOWN_LIST))
        # endregion

        # Step 2
        menu_page.click_default_client_dropdown()
        self.verify(f"Step 2 - Verify clients attached to {self.login1}: {self.client1_1}",
                    None, menu_page.wait_element_presence(menu_page.get_default_client_selection_xpath(self.client1_1)))
        self.verify(f"Step 2 - Verify clients attached to {self.login1}: {self.client1_2}",
                    None, menu_page.wait_element_presence(menu_page.get_default_client_selection_xpath(self.client1_2)))
        self.verify(f"Step 2 - Verify clients attached to {self.login1}: {self.client1_3}",
                    None, menu_page.wait_element_presence(menu_page.get_default_client_selection_xpath(self.client1_3)))
        # endregion

        # Step 3
        menu_page.click_default_client_selection(self.client1_1)
        self.verify(f"Step 3 - {self.client1_1} is set as default client", self.client1_1, menu_page.get_default_client())
        # endregion

        # Step 4
        menu_page.click_keyboard("Back")
        menu_page.click_on_logout()
        self.verify(f'Step 4 - Login Page is opened', None, menu_page.wait_element_presence(LoginConstants.LOGIN_TITLE))
        # endregion

        # Step 5
        login_page.login_to_mobile_trading(self.login3, self.password1)
        self.verify("Step 5 - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # Step 6
        main_page.click_on_menu()
        menu_page.click_on_preferences()
        self.verify("Step 6 - Preferences is opened", None,
                    menu_page.wait_element_presence(MenuConstants.PREFERENCES_TITLE))
        self.verify("Step 6 - Default Client title is shown", None,
                    menu_page.wait_element_presence(MenuConstants.DEFAULT_CLIENT_TITLE))
        self.verify("Step 6 - Default Client dropdown is shown", None,
                    menu_page.wait_element_presence(MenuConstants.DEFAULT_CLIENT_DROP_DOWN_LIST))
        # endregion

        # Step 7
        menu_page.click_default_client_dropdown()
        self.verify(f"Step 7 - Verify clients attached to {self.login3}: {self.client2_1}",
                    None, menu_page.wait_element_presence(menu_page.get_default_client_selection_xpath(self.client2_1)))
        self.verify(f"Step 7 - Verify clients attached to {self.login3}: {self.client2_2}",
                    None, menu_page.wait_element_presence(menu_page.get_default_client_selection_xpath(self.client2_2)))
        # endregion

        # region - postconditions
        # endregion