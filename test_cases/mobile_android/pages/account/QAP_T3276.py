from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3276(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # region - test details

        # Step 1
        main_page.click_on_menu()
        menu_page.click_on_personal_details()
        self.verify("Step 1 - Personal Details is opened", None, menu_page.wait_element_presence(MenuConstants.PERSONAL_DETAILS_TITLE))
        # endregion

        # Step 2
        menu_page.set_preferred_communication_method("Mobile No")
        menu_page.click_pd_mobile_no()
        # menu_page.wait_edit_mode(MenuConstants.PD_MOBILE_NO)
        menu_page.clear_pd_mobile_no()
        self.verify("Step 2 - Mobile No field is clear", "Mobile No", menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_MOBILE_NO, "text"))
        # endregion

        # Step 3
        menu_page.click_pd_go_back()
        self.verify("Step 3 - User Profile is opened", None, menu_page.wait_element_presence(MenuConstants.USER_PROFILE_TITLE))
        # endregion

        # Step 4
        menu_page.click_on_personal_details()
        self.verify("Step 4 - Preferred Communication Method: Mobile No", None,
                    menu_page.wait_element_presence(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_MOBILE_NO))
        self.verify("Step 4 - Mobile No: 123456789", "123456789, Mobile No",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_MOBILE_NO, "text"))
        self.verify("Step 4 - Email: mail@quodfinancial.com", "mail@quodfinancial.com, Email",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_EMAIL, "text"))
        # endregion

        # Step 5
        menu_page.set_preferred_communication_method("Email")
        menu_page.click_pd_email()
        # menu_page.wait_edit_mode(MenuConstants.PD_EMAIL)
        menu_page.clear_pd_email()
        self.verify("Step 5 - Email field is clear", "Email",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_EMAIL, "text"))
        # endregion

        # Step 6
        menu_page.click_pd_go_back()
        menu_page.click_on_personal_details()
        self.verify("Step 6 - Preferred Communication Method: Email", None,
                    menu_page.wait_element_presence(
                        MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_EMAIL))
        self.verify("Step 6 - Mobile No: 123456789", "123456789, Mobile No",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_MOBILE_NO, "text"))
        self.verify("Step 6 - Email: mail@quodfinancial.com", "mail@quodfinancial.com, Email",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_EMAIL, "text"))
        # endregion

        # Step 7

        # endregion
        menu_page.set_preferred_communication_method("Email")
        menu_page.pd_fill_mobile_no("123")
        menu_page.pd_fill_email("a@b.c")
        menu_page.click_pd_go_back()
        menu_page.click_on_personal_details()
        self.verify("Step 7 - Preferred Communication Method: Email", None,
                    menu_page.wait_element_presence(
                        MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_EMAIL))
        self.verify("Step 7 - Mobile No: 123", "123, Mobile No",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_MOBILE_NO, "text"))
        self.verify("Step 7 - Email: a@b.c", "a@b.c, Email",
                    menu_page.get_attribute_of_element_by_xpath(MenuConstants.PD_EMAIL, "text"))
        # region - postconditions
        # endregion